import time

from enum import Enum
from typing import Any, IO, List, Tuple, Union

from dolreader.dol import DolFile


def _align_bytes(_bytes: bytes, alignment: int = 4, fill: bytes = b"\x00") -> bytes:
    length = len(_bytes)
    diff = alignment - (length % alignment)
    return _bytes + (fill * diff)


class InvalidGeckoCodeError(Exception):
    pass


class GeckoCode(object):
    class Type(Enum):
        WRITE_8 = 0x00
        WRITE_16 = 0x02
        WRITE_32 = 0x04
        WRITE_STR = 0x06
        WRITE_SERIAL = 0x08
        IF_EQ_32 = 0x20
        IF_NEQ_32 = 0x22
        IF_GT_32 = 0x24
        IF_LT_32 = 0x26
        IF_EQ_16 = 0x28
        IF_NEQ_16 = 0x2A
        IF_GT_16 = 0x2C
        IF_LT_16 = 0x2E
        BASE_ADDR_LOAD = 0x40
        BASE_ADDR_SET = 0x42
        BASE_ADDR_STORE = 0x44
        BASE_GET_NEXT = 0x46
        PTR_ADDR_LOAD = 0x48
        PTR_ADDR_SET = 0x4A
        PTR_ADDR_STORE = 0x4C
        PTR_GET_NEXT = 0x4E
        REPEAT_SET = 0x60
        REPEAT_EXEC = 0x62
        RETURN = 0x64
        GOTO = 0x66
        GOSUB = 0x68
        GECKO_REG_SET = 0x80
        GECKO_REG_LOAD = 0x82
        GECKO_REG_STORE = 0x84
        GECKO_REG_OPERATE_I = 0x86
        GECKO_REG_OPERATE = 0x88
        MEMCPY_1 = 0x8A
        MEMCPY_2 = 0x8C
        GECKO_IF_EQ_16 = 0xA0
        GECKO_IF_NEQ_16 = 0xA2
        GECKO_IF_GT_16 = 0xA4
        GECKO_IF_LT_16 = 0xA6
        COUNTER_IF_EQ_16 = 0xA8
        COUNTER_IF_NEQ_16 = 0xAA
        COUNTER_IF_GT_16 = 0xAC
        COUNTER_IF_LT_16 = 0xAE
        ASM_EXECUTE = 0xC0
        ASM_INSERT = 0xC2
        ASM_INSERT_L = 0xC4
        WRITE_BRANCH = 0xC6
        SWITCH = 0xCC
        ADDR_RANGE_CHECK = 0xCE
        TERMINATOR = 0xE0
        ENDIF = 0xE2
        EXIT = 0xF0
        ASM_INSERT_XOR = 0xF2
        BRAINSLUG_SEARCH = 0xF6

    class ArithmeticType(Enum):
        ADD = 0
        MUL = 1
        OR = 2
        AND = 3
        XOR = 4
        SLW = 5
        SRW = 6
        ROL = 7
        ASR = 8
        FADDS = 9
        FMULS = 10

    @staticmethod
    def int_to_type(id: int) -> Type:
        id &= 0xFE
        if id == 0xF4:
            return GeckoCode.Type.ASM_INSERT_XOR
        elif id >= 0xF0:
            return GeckoCode.Type(id & 0xFE)
        else:
            return GeckoCode.Type(id & 0xEE)

    @staticmethod
    def type_to_int(ty: Type) -> int:
        return ty.value

    @staticmethod
    def is_ifblock(_type: Union[Type, "GeckoCode"]) -> bool:
        if isinstance(_type, GeckoCode):
            _type = _type.codetype

        return _type in {
            GeckoCode.Type.IF_EQ_32,
            GeckoCode.Type.IF_NEQ_32,
            GeckoCode.Type.IF_GT_32,
            GeckoCode.Type.IF_LT_32,
            GeckoCode.Type.IF_EQ_16,
            GeckoCode.Type.IF_NEQ_16,
            GeckoCode.Type.IF_GT_16,
            GeckoCode.Type.IF_LT_16,
            GeckoCode.Type.GECKO_IF_EQ_16,
            GeckoCode.Type.GECKO_IF_NEQ_16,
            GeckoCode.Type.GECKO_IF_GT_16,
            GeckoCode.Type.GECKO_IF_LT_16,
            GeckoCode.Type.COUNTER_IF_EQ_16,
            GeckoCode.Type.COUNTER_IF_NEQ_16,
            GeckoCode.Type.COUNTER_IF_GT_16,
            GeckoCode.Type.COUNTER_IF_LT_16,
            GeckoCode.Type.BRAINSLUG_SEARCH
        }

    @staticmethod
    def is_multiline(_type: Union[Type, "GeckoCode"]) -> bool:
        if isinstance(_type, GeckoCode):
            _type = _type.codetype

        return _type in {
            GeckoCode.Type.WRITE_STR,
            GeckoCode.Type.WRITE_SERIAL,
            GeckoCode.Type.ASM_EXECUTE,
            GeckoCode.Type.ASM_INSERT,
            GeckoCode.Type.ASM_INSERT_L,
            GeckoCode.Type.ASM_INSERT_XOR,
            GeckoCode.Type.BRAINSLUG_SEARCH
        }

    @staticmethod
    def can_preprocess(_type: Union[Type, "GeckoCode"]) -> bool:
        if isinstance(_type, GeckoCode):
            _type = _type.codetype

        return _type in {
            GeckoCode.Type.WRITE_8,
            GeckoCode.Type.WRITE_16,
            GeckoCode.Type.WRITE_32,
            GeckoCode.Type.WRITE_STR,
            GeckoCode.Type.WRITE_SERIAL,
            GeckoCode.Type.WRITE_BRANCH
        }

    @staticmethod
    def assertRegister(gr: int):
        assert 0 <= gr < 16, f"Only Gecko Registers 0-15 are allowed ({gr} is beyond range)"

    @staticmethod
    def typeof(code: "GeckoCode") -> Type:
        return code.codetype
    _counter = 0

    @staticmethod
    def bytes_to_geckocode(f: IO) -> "GeckoCode":
        def add_children_till_terminator(code: "GeckoCode", f: IO):
            while True:
                try:
                    child = GeckoCode.bytes_to_geckocode(f)
                    if child.codetype in {GeckoCode.Type.TERMINATOR, GeckoCode.Type.EXIT}:
                        f.seek(-8, 1)
                        return
                    code.add_child(child)
                except Exception:
                    return

        metadata = f.read(4)
        address = 0x80000000 | (int.from_bytes(
            metadata, byteorder="big", signed=False) & 0x1FFFFFF)
        codetype = GeckoCode.int_to_type((int.from_bytes(
            metadata, "big", signed=False) >> 24) & 0xFE)
        isPointerType = ((int.from_bytes(
            metadata, "big", signed=False) >> 24) & 0x10 != 0)

        if codetype == GeckoCode.Type.WRITE_8:
            info = f.read(4)
            value = int.from_bytes(info[3:], "big", signed=False)
            repeat = int.from_bytes(info[:2], "big", signed=False)
            return Write8(value, repeat, address, isPointerType)
        elif codetype == GeckoCode.Type.WRITE_16:
            info = f.read(4)
            value = int.from_bytes(info[2:], "big", signed=False)
            repeat = int.from_bytes(info[:2], "big", signed=False)
            return Write16(value, repeat, address, isPointerType)
        elif codetype == GeckoCode.Type.WRITE_32:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            return Write32(value, address, isPointerType)
        elif codetype == GeckoCode.Type.WRITE_STR:
            size = int.from_bytes(f.read(4), "big", signed=False)
            return WriteString(f.read(size), address, isPointerType)
        elif codetype == GeckoCode.Type.WRITE_SERIAL:
            info = f.read(12)
            value = int.from_bytes(info[:4], "big", signed=False)
            valueSize = int.from_bytes(info[4:5], "big", signed=False) >> 4
            repeat = int.from_bytes(info[4:5], "big", signed=False) & 0xF
            addressInc = int.from_bytes(info[6:8], "big", signed=False)
            valueInc = int.from_bytes(info[8:], "big", signed=False)
            return WriteSerial(value, repeat, address, isPointerType, valueSize, addressInc, valueInc)
        elif codetype == GeckoCode.Type.IF_EQ_32:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            _code = IfEqual32(value, address, endif=(address & 1) == 1)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.IF_NEQ_32:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            _code = IfNotEqual32(value, address, endif=(address & 1) == 1)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.IF_GT_32:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            _code = IfGreaterThan32(value, address, endif=(address & 1) == 1)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.IF_LT_32:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            _code = IfLesserThan32(value, address, endif=(address & 1) == 1)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.IF_EQ_16:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            mask = (int.from_bytes(info, "big", signed=False) >> 16) & 0xFFFF
            _code = IfEqual16(value, address, endif=(address & 1) == 1, mask=mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.IF_NEQ_16:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            mask = (int.from_bytes(info, "big", signed=False) >> 16) & 0xFFFF
            _code = IfNotEqual16(value, address, endif=(address & 1) == 1, mask=mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.IF_GT_16:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            mask = (int.from_bytes(info, "big", signed=False) >> 16) & 0xFFFF
            _code = IfGreaterThan16(value, address, endif=(address & 1) == 1, mask=mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.IF_LT_16:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            mask = (int.from_bytes(info, "big", signed=False) >> 16) & 0xFFFF
            _code = IfLesserThan16(value, address, endif=(address & 1) == 1, mask=mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.BASE_ADDR_LOAD:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return BaseAddressLoad(value, flags & 0x01110000, flags & 0xF, isPointerType)
        elif codetype == GeckoCode.Type.BASE_ADDR_SET:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return BaseAddressSet(value, flags & 0x01110000, flags & 0xF, isPointerType)
        elif codetype == GeckoCode.Type.BASE_ADDR_STORE:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return BaseAddressStore(value, flags & 0x00110000, flags & 0xF, isPointerType)
        elif codetype == GeckoCode.Type.BASE_GET_NEXT:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return BaseAddressGetNext(value)
        elif codetype == GeckoCode.Type.PTR_ADDR_LOAD:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return PointerAddressLoad(value, flags & 0x01110000, flags & 0xF, isPointerType)
        elif codetype == GeckoCode.Type.PTR_ADDR_SET:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return PointerAddressSet(value, flags & 0x01110000, flags & 0xF, isPointerType)
        elif codetype == GeckoCode.Type.PTR_ADDR_STORE:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return PointerAddressStore(value, flags & 0x00110000, flags & 0xF, isPointerType)
        elif codetype == GeckoCode.Type.PTR_GET_NEXT:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = int.from_bytes(metadata, "big", signed=False)
            return PointerAddressGetNext(value)
        elif codetype == GeckoCode.Type.REPEAT_SET:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xF
            repeat = int.from_bytes(metadata, "big", signed=False) & 0xFFFF
            return SetRepeat(repeat, value)
        elif codetype == GeckoCode.Type.REPEAT_EXEC:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xF
            return ExecuteRepeat(value)
        elif codetype == GeckoCode.Type.RETURN:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xF
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00300000) >> 20
            return Return(value)
        elif codetype == GeckoCode.Type.GOTO:
            info = f.read(4)
            value = int.from_bytes(metadata, "big", signed=False) & 0xFFFF
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00300000) >> 20
            return Goto(flags, value)
        elif codetype == GeckoCode.Type.GOSUB:
            info = f.read(4)
            value = int.from_bytes(metadata, "big", signed=False) & 0xFFFF
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00300000) >> 20
            register = int.from_bytes(info, "big", signed=False) & 0xF
            return Gosub(flags, value, register)
        elif codetype == GeckoCode.Type.GECKO_REG_SET:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00110000) >> 16
            register = int.from_bytes(metadata, "big", signed=False) & 0xF
            return GeckoRegisterSet(value, flags, register, isPointerType)
        elif codetype == GeckoCode.Type.GECKO_REG_LOAD:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00310000) >> 16
            register = int.from_bytes(metadata, "big", signed=False) & 0xF
            return GeckoRegisterLoad(value, flags, register, isPointerType)
        elif codetype == GeckoCode.Type.GECKO_REG_STORE:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00310000) >> 16
            register = int.from_bytes(metadata, "big", signed=False) & 0xF
            repeat = (int.from_bytes(metadata, "big",
                                     signed=False) & 0xFFF0) >> 4
            return GeckoRegisterStore(value, repeat, flags, register, isPointerType)
        elif codetype == GeckoCode.Type.GECKO_REG_OPERATE_I:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00030000) >> 16
            register = int.from_bytes(metadata, "big", signed=False) & 0xF
            opType = GeckoCode.ArithmeticType(
                (int.from_bytes(metadata, "big", signed=False) & 0x00F00000) >> 18)
            return GeckoRegisterOperateI(value, opType, flags, register)
        elif codetype == GeckoCode.Type.GECKO_REG_OPERATE:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False) & 0xF
            flags = (int.from_bytes(metadata, "big",
                                    signed=False) & 0x00030000) >> 16
            register = int.from_bytes(metadata, "big", signed=False) & 0xF
            opType = GeckoCode.ArithmeticType(
                (int.from_bytes(metadata, "big", signed=False) & 0x00F00000) >> 18)
            return GeckoRegisterOperate(value, opType, flags, register)
        elif codetype == GeckoCode.Type.MEMCPY_1:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            size = (int.from_bytes(metadata, "big",
                                   signed=False) & 0x00FFFF00) >> 8
            register = (int.from_bytes(
                metadata, "big", signed=False) & 0xF0) >> 4
            otherRegister = int.from_bytes(metadata, "big", signed=False) & 0xF
            return MemoryCopyTo(value, size, otherRegister, register, isPointerType)
        elif codetype == GeckoCode.Type.MEMCPY_2:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            size = (int.from_bytes(metadata, "big",
                                   signed=False) & 0x00FFFF00) >> 8
            register = (int.from_bytes(
                metadata, "big", signed=False) & 0xF0) >> 4
            otherRegister = int.from_bytes(metadata, "big", signed=False) & 0xF
            return MemoryCopyFrom(value, size, otherRegister, register, isPointerType)
        elif codetype == GeckoCode.Type.GECKO_IF_EQ_16:
            info = f.read(4)
            register = (int.from_bytes(info, "big", signed=False)
                        & 0x0F000000) >> 24
            otherRegister = (int.from_bytes(
                info, "big", signed=False) & 0xF0000000) >> 28
            mask = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = GeckoIfEqual16(
                address, register, otherRegister, isPointerType, (address & 1) == 1, mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.GECKO_IF_NEQ_16:
            info = f.read(4)
            register = (int.from_bytes(info, "big", signed=False)
                        & 0x0F000000) >> 24
            otherRegister = (int.from_bytes(
                info, "big", signed=False) & 0xF0000000) >> 28
            mask = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = GeckoIfNotEqual16(
                address, register, otherRegister, isPointerType, (address & 1) == 1, mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.GECKO_IF_GT_16:
            info = f.read(4)
            register = (int.from_bytes(info, "big", signed=False)
                        & 0x0F000000) >> 24
            otherRegister = (int.from_bytes(
                info, "big", signed=False) & 0xF0000000) >> 28
            mask = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = GeckoIfGreaterThan16(
                address, register, otherRegister, isPointerType, (address & 1) == 1, mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.GECKO_IF_LT_16:
            info = f.read(4)
            register = (int.from_bytes(info, "big", signed=False)
                        & 0x0F000000) >> 24
            otherRegister = (int.from_bytes(
                info, "big", signed=False) & 0xF0000000) >> 28
            mask = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = GeckoIfLesserThan16(
                address, register, otherRegister, isPointerType, (address & 1) == 1, mask)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.COUNTER_IF_EQ_16:
            info = f.read(4)
            counter = (int.from_bytes(metadata, "big",
                                      signed=False) & 0xFFFF0) >> 4
            flags = int.from_bytes(metadata, "big", signed=False) & 9
            mask = (int.from_bytes(info, "big", signed=False) & 0xFFFF0000) >> 16
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = CounterIfEqual16(value, mask, flags, counter)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.COUNTER_IF_NEQ_16:
            info = f.read(4)
            counter = (int.from_bytes(metadata, "big",
                                      signed=False) & 0xFFFF0) >> 4
            flags = int.from_bytes(metadata, "big", signed=False) & 9
            mask = (int.from_bytes(info, "big", signed=False) & 0xFFFF0000) >> 16
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = CounterIfNotEqual16(value, mask, flags, counter)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.COUNTER_IF_GT_16:
            info = f.read(4)
            counter = (int.from_bytes(metadata, "big",
                                      signed=False) & 0xFFFF0) >> 4
            flags = int.from_bytes(metadata, "big", signed=False) & 9
            mask = (int.from_bytes(info, "big", signed=False) & 0xFFFF0000) >> 16
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = CounterIfGreaterThan16(value, mask, flags, counter)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.COUNTER_IF_LT_16:
            info = f.read(4)
            counter = (int.from_bytes(metadata, "big",
                                      signed=False) & 0xFFFF0) >> 4
            flags = int.from_bytes(metadata, "big", signed=False) & 9
            mask = (int.from_bytes(info, "big", signed=False) & 0xFFFF0000) >> 16
            value = int.from_bytes(info, "big", signed=False) & 0xFFFF
            _code = CounterIfLesserThan16(value, mask, flags, counter)
            add_children_till_terminator(_code, f)
            return _code
        elif codetype == GeckoCode.Type.ASM_EXECUTE:
            info = f.read(4)
            size = int.from_bytes(info, "big", signed=False)
            return AsmExecute(f.read(size << 3))
        elif codetype == GeckoCode.Type.ASM_INSERT:
            info = f.read(4)
            size = int.from_bytes(info, "big", signed=False)
            return AsmInsert(f.read(size << 3), address, isPointerType)
        elif codetype == GeckoCode.Type.ASM_INSERT_L:
            info = f.read(4)
            size = int.from_bytes(info, "big", signed=False)
            return AsmInsertLink(f.read(size << 3), address, isPointerType)
        elif codetype == GeckoCode.Type.WRITE_BRANCH:
            info = f.read(4)
            dest = int.from_bytes(info, "big", signed=False)
            return WriteBranch(dest, address, isPointerType)
        elif codetype == GeckoCode.Type.SWITCH:
            return Switch()
        elif codetype == GeckoCode.Type.ADDR_RANGE_CHECK:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            endif = int.from_bytes(metadata, "big", signed=False) & 0x1
            return AddressRangeCheck(value, isPointerType, endif)
        elif codetype == GeckoCode.Type.TERMINATOR:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            return Terminator(value)
        elif codetype == GeckoCode.Type.ENDIF:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            inverse = (int.from_bytes(metadata, "big",
                                      signed=False) & 0x00F00000) >> 24
            numEndifs = int.from_bytes(metadata, "big", signed=False) & 0xFF
            return Endif(value, inverse, numEndifs)
        elif codetype == GeckoCode.Type.EXIT:
            f.seek(4, 1)
            return Exit()
        elif codetype == GeckoCode.Type.ASM_INSERT_XOR:
            info = f.read(4)
            size = int.from_bytes(info, "big", signed=False) & 0x000000FF
            xor = int.from_bytes(info, "big", signed=False) & 0x00FFFF00
            num = int.from_bytes(info, "big", signed=False) & 0xFF000000
            pointer = codetype.value == 0xF4
            return AsmInsertXOR(f.read(size << 3), address, pointer, xor, num)
        elif codetype == GeckoCode.Type.BRAINSLUG_SEARCH:
            info = f.read(4)
            value = int.from_bytes(info, "big", signed=False)
            size = int.from_bytes(metadata, "big", signed=False) & 0x000000FF
            _code = BrainslugSearch(f.read(size << 3), address, [
                                    (value & 0xFFFF0000) >> 16, value & 0xFFFF])
            add_children_till_terminator(_code, f)
            return _code

    def __init__(self):
        raise InvalidGeckoCodeError(
            f"Cannot instantiate abstract type {self.__class__.__name__}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self) -> str:
        return self.__class__.__name__

    def __len__(self) -> int:
        return 0

    def __iter__(self):
        self._iterpos = 0
        return self

    def __next__(self) -> Union[int, bytes, "GeckoCode"]:
        try:
            self._iterpos += 1
            return self[self._iterpos-1]
        except IndexError:
            raise StopIteration

    def __getitem__(self, index: int) -> Any:
        raise IndexError

    def __setitem__(self, index: int, value: Any):
        raise IndexError

    def __hash__(self) -> str:
        return str(self)

    @property
    def children(self) -> List["GeckoCode"]:
        return []

    @property
    def codetype(self) -> Type:
        return None

    @property
    def value(self) -> Union[int, bytes]:
        return None

    @value.setter
    def value(self, value: Union[int, bytes]):
        pass

    def add_child(self, child: "GeckoCode"):
        pass

    def remove_child(self, child: "GeckoCode"):
        pass

    def virtual_length(self) -> int:
        return 0

    def populate_from_bytes(self, f: IO):
        pass

    def apply(self, dol: DolFile) -> bool:
        return False

    def as_bytes(self) -> bytes:
        return b""

    def as_text(self) -> str:
        packet = self.as_bytes()
        nibbles = [packet[i:i+4] for i in range(0, len(packet), 4)]
        stringRepr = ""
        for i, nibble in enumerate(nibbles):
            if i > 0:
                if i % 2:
                    stringRepr += f" {nibble.hex()}"
                else:
                    stringRepr += f"\n{nibble.hex()}"
            else:
                stringRepr += f"{nibble.hex()}"
        return stringRepr.upper()


class Write8(GeckoCode):
    def __init__(self, value: Union[int, bytes], repeat: int = 0, address: int = 0, isPointer: bool = False):
        self.value = value
        self._address = address
        self._repeat = repeat
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        if self._repeat > 0:
            return f"({intType:02X}) Write byte 0x{self.value:02X} to (0x{self._address:08X} + the {addrstr}) {self._repeat + 1} times consecutively"
        else:
            return f"({intType:02X}) Write byte 0x{self.value:02X} to 0x{self._address:08X} + the {addrstr}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.WRITE_8

    @property
    def value(self) -> int:
        return self._value & 0xFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFF

    def virtual_length(self) -> int:
        return 1

    def apply(self, dol: DolFile) -> bool:
        addr = self._address | 0x80000000
        if dol.is_mapped(addr):
            dol.seek(addr)
            counter = self._repeat
            while counter + 1 > 0:
                dol.write(self.value.to_bytes(1, "big", signed=False))
                counter -= 1
            return True
        return False

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFF)
        info = (self._repeat << 16) | self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Write16(GeckoCode):
    def __init__(self, value: Union[int, bytes], repeat: int = 0, address: int = 0, isPointer: bool = False):
        self.value = value
        self._address = address
        self._repeat = repeat
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        if self._repeat > 0:
            return f"({intType:02X}) Write short 0x{self.value:04X} to (0x{self._address:08X} + the {addrstr}) {self._repeat + 1} times consecutively"
        else:
            return f"({intType:02X}) Write short 0x{self.value:04X} to 0x{self._address:08X} + the {addrstr}"

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.WRITE_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def virtual_length(self) -> int:
        return 1

    def apply(self, dol: DolFile) -> bool:
        addr = self._address | 0x80000000
        if dol.is_mapped(addr):
            dol.seek(addr)
            counter = self._repeat
            while counter + 1 > 0:
                dol.write(self.value.to_bytes(2, "big", signed=False))
                counter -= 1
            return True
        return False

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE)
        info = (self._repeat << 16) | self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Write32(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False):
        self.value = value
        self._address = address
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        return f"({intType:02X}) Write word 0x{self.value:08X} to 0x{self._address:08X} + the {addrstr}"

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.WRITE_32

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def apply(self, dol: DolFile) -> bool:
        addr = self._address | 0x80000000
        if dol.is_mapped(addr):
            dol.seek(addr)
            dol.write(self.value.to_bytes(4, "big", signed=False))
            return True
        return False

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC)
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class WriteString(GeckoCode):
    def __init__(self, value: bytes, address: int = 0, isPointer: bool = False):
        self.value = value
        self._address = address
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 8 + len(self.value)

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        return f"({intType:02X}) Write {len(self) - 8} bytes to 0x{self._address:08X} + the {addrstr}"

    def __getitem__(self, index: int) -> bytes:
        return self.value[index]

    def __setitem__(self, index: int, value: bytes):
        if isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")
        self.value[index] = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.WRITE_STR

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        self._value = value

    def virtual_length(self) -> int:
        return ((len(self) + 7) & -0x8) >> 3

    def apply(self, dol: DolFile) -> bool:
        addr = self._address | 0x80000000
        if dol.is_mapped(addr):
            dol.seek(addr)
            dol.write(self.value)
            return True
        return False

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFF)
        info = len(self.value)
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + _align_bytes(self.value, alignment=8)


class WriteSerial(GeckoCode):
    def __init__(self, value: Union[int, bytes], repeat: int = 0, address: int = 0, isPointer: bool = False,
                 valueSize: int = 2, addrInc: int = 4, valueInc: int = 0):
        self.value = value
        self.valueInc = valueInc
        self._valueSize = valueSize
        self._address = address
        self._addressInc = addrInc
        self._repeat = repeat
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 16

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        valueType = ("byte", "short", "word")[self._valueSize]
        if self._repeat > 0:
            mapping = f"incrementing the value by {self.valueInc} and the address by {self._addressInc} each iteration"
            return f"({intType:02X}) Write {valueType} 0x{self.value:08X} to (0x{self._address:08X} + the {addrstr}) {self._repeat + 1} times consecutively, {mapping}"
        else:
            return f"({intType:02X}) Write {valueType} 0x{self.value:08X} to 0x{self._address:08X} + the {addrstr})"

    def __getitem__(self, index: int) -> Tuple[int, int]:
        if index >= self._repeat:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif index < 0:
            index += self._repeat

        return (self._address + self._addressInc*index,
                self.value + self.valueInc*index)

    def __setitem__(self, index: int, value: Any):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.WRITE_SERIAL

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 2

    def apply(self, dol: DolFile) -> bool:
        addr = self._address | 0x80000000
        if dol.is_mapped(addr):
            for addr, value in self:
                dol.seek(addr)
                dol.write(value)
            return True
        return False

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFF)
        info = self.value
        subinfo = (self._valueSize << 28) | (
            self._repeat << 16) | (self._addressInc)
        valueInc = self.valueInc
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + subinfo.to_bytes(4, "big", signed=False) + valueInc.to_bytes(4, "big", signed=False)


class IfEqual32(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False):
        self.value = value
        self._address = address
        self._endif = endif
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the word at address (0x{self._address:08X} + the {addrstr}) is equal to 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_EQ_32

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC) | (1 if self._endif else 0)
        info = self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class IfNotEqual32(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False):
        self.value = value
        self._address = address
        self._endif = endif
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the word at address (0x{self._address:08X} + the {addrstr}) is not equal to 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_NEQ_32

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC) | (1 if self._endif else 0)
        info = self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class IfGreaterThan32(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False):
        self.value = value
        self._address = address
        self._endif = endif
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the word at address (0x{self._address:08X} + the {addrstr}) is greater than 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_GT_32

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC) | (1 if self._endif else 0)
        info = self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class IfLesserThan32(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False):
        self.value = value
        self._address = address
        self._endif = endif
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the word at address (0x{self._address:08X} + the {addrstr}) is lesser than 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_LT_32

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC) | (1 if self._endif else 0)
        info = self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class IfEqual16(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False, mask: int = 0xFFFF):
        self.value = value
        self._address = address
        self._endif = endif
        self._mask = mask
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the short at address (0x{self._address:08X} + the {addrstr}) & ~0x{self._mask:04X} is equal to 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_EQ_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class IfNotEqual16(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False, mask: int = 0xFFFF):
        self.value = value
        self._address = address
        self._endif = endif
        self._mask = mask
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the short at address (0x{self._address:08X} + the {addrstr}) & ~0x{self._mask:04X} is not equal to 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_NEQ_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class IfGreaterThan16(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False, mask: int = 0xFFFF):
        self.value = value
        self._address = address
        self._endif = endif
        self._mask = mask
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the short at address (0x{self._address:08X} + the {addrstr}) & ~0x{self._mask:04X} is greater than 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_GT_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class IfLesserThan16(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False,
                 endif: bool = False, mask: int = 0xFFFF):
        self.value = value
        self._address = address
        self._endif = endif
        self._mask = mask
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If the short at address (0x{self._address:08X} + the {addrstr}) & ~0x{self._mask:04X} is lesser than 0x{self.value:08X}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.IF_LT_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class BaseAddressLoad(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x000:
            return f"({intType:02X}) Set the base address to the value at address [0x{self.value:08X}]"
        elif flags == 0x001:
            return f"({intType:02X}) Set the base address to the value at address [gr{self._register} + 0x{self.value:08X}]"
        elif flags == 0x010:
            return f"({intType:02X}) Set the base address to the value at address [{addrstr} + 0x{self.value:08X}]"
        elif flags == 0x011:
            return f"({intType:02X}) Set the base address to the value at address [{addrstr} + gr{self._register} + 0x{self.value:08X}]"
        elif flags == 0x100:
            return f"({intType:02X}) Add the value at address [0x{self.value:08X}] to the base address"
        elif flags == 0x101:
            return f"({intType:02X}) Add the value at address [gr{self._register} + 0x{self.value:08X}] to the base address"
        elif flags == 0x110:
            return f"({intType:02X}) Add the value at address [{addrstr} + 0x{self.value:08X}] to the base address"
        elif flags == 0x111:
            return f"({intType:02X}) Add the value at address [{addrstr} + gr{self._register} + 0x{self.value:08X}] to the base address"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.BASE_ADDR_LOAD

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class BaseAddressSet(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x000:
            return f"({intType:02X}) Set the base address to the value 0x{self.value:08X}"
        elif flags == 0x001:
            return f"({intType:02X}) Set the base address to the value (gr{self._register} + 0x{self.value:08X})"
        elif flags == 0x010:
            return f"({intType:02X}) Set the base address to the value ({addrstr} + 0x{self.value:08X})"
        elif flags == 0x011:
            return f"({intType:02X}) Set the base address to the value ({addrstr} + gr{self._register} + 0x{self.value:08X})"
        elif flags == 0x100:
            return f"({intType:02X}) Add the value 0x{self.value:08X} to the base address"
        elif flags == 0x101:
            return f"({intType:02X}) Add the value (gr{self._register} + 0x{self.value:08X}) to the base address"
        elif flags == 0x110:
            return f"({intType:02X}) Add the value ({addrstr} + 0x{self.value:08X}) to the base address"
        elif flags == 0x111:
            return f"({intType:02X}) Add the value ({addrstr} + gr{self._register}) + 0x{self.value:08X} to the base address"
        return f"({intType:02X}) Invalid flag {flags}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.BASE_ADDR_SET

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class BaseAddressStore(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x000:
            return f"({intType:02X}) Store the base address at address [0x{self.value:08X}]"
        elif flags == 0x001:
            return f"({intType:02X}) Store the base address at address [gr{self._register} + 0x{self.value:08X}]"
        elif flags == 0x010:
            return f"({intType:02X}) Store the base address at address [{addrstr} + 0x{self.value:08X}]"
        elif flags == 0x011:
            return f"({intType:02X}) Store the base address at address [{addrstr} + gr{self._register} + 0x{self.value:08X}]"
        return f"({intType:02X}) Invalid flag {flags}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.BASE_ADDR_STORE

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class BaseAddressGetNext(GeckoCode):
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) Set the base address to be the next Gecko Code's address + {self.value:04X}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.BASE_GET_NEXT

    @property
    def value(self) -> int:
        return self.value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self.value = value & 0xFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | self.value
        return metadata.to_bytes(4, "big", signed=False) + b"\x00\x00\x00\x00"


class PointerAddressLoad(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x000:
            return f"({intType:02X}) Set the pointer address to the value at address [0x{self.value:08X}]"
        elif flags == 0x001:
            return f"({intType:02X}) Set the pointer address to the value at address [gr{self._register} + 0x{self.value:08X}]"
        elif flags == 0x010:
            return f"({intType:02X}) Set the pointer address to the value at address [{addrstr} + 0x{self.value:08X}]"
        elif flags == 0x011:
            return f"({intType:02X}) Set the pointer address to the value at address [{addrstr} + gr{self._register} + 0x{self.value:08X}]"
        elif flags == 0x100:
            return f"({intType:02X}) Add the value at address [0x{self.value:08X}] to the pointer address"
        elif flags == 0x101:
            return f"({intType:02X}) Add the value at address [gr{self._register} + 0x{self.value:08X}] to the pointer address"
        elif flags == 0x110:
            return f"({intType:02X}) Add the value at address [{addrstr} + 0x{self.value:08X}] to the pointer address"
        elif flags == 0x111:
            return f"({intType:02X}) Add the value at address [{addrstr} + gr{self._register} + 0x{self.value:08X}] to the pointer address"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.PTR_ADDR_LOAD

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class PointerAddressSet(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x000:
            return f"({intType:02X}) Set the pointer address to the value 0x{self.value:08X}"
        elif flags == 0x001:
            return f"({intType:02X}) Set the pointer address to the value (gr{self._register} + 0x{self.value:08X})"
        elif flags == 0x010:
            return f"({intType:02X}) Set the pointer address to the value ({addrstr} + 0x{self.value:08X})"
        elif flags == 0x011:
            return f"({intType:02X}) Set the pointer address to the value ({addrstr} + gr{self._register} + 0x{self.value:08X})"
        elif flags == 0x100:
            return f"({intType:02X}) Add the value 0x{self.value:08X} to the pointer address"
        elif flags == 0x101:
            return f"({intType:02X}) Add the value (gr{self._register} + 0x{self.value:08X}) to the pointer address"
        elif flags == 0x110:
            return f"({intType:02X}) Add the value ({addrstr} + 0x{self.value:08X}) to the pointer address"
        elif flags == 0x111:
            return f"({intType:02X}) Add the value ({addrstr} + gr{self._register}) + 0x{self.value:08X} to the pointer address"
        return f"({intType:02X}) Invalid flag {flags}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.PTR_ADDR_SET

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class PointerAddressStore(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x000:
            return f"({intType:02X}) Store the pointer address at address [0x{self.value:08X}]"
        elif flags == 0x001:
            return f"({intType:02X}) Store the pointer address at address [gr{self._register} + 0x{self.value:08X}]"
        elif flags == 0x010:
            return f"({intType:02X}) Store the pointer address at address [{addrstr} + 0x{self.value:08X}]"
        elif flags == 0x011:
            return f"({intType:02X}) Store the pointer address at address [{addrstr} + gr{self._register} + 0x{self.value:08X}]"
        return f"({intType:02X}) Invalid flag {flags}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.PTR_ADDR_STORE

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class PointerAddressGetNext(GeckoCode):
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) Set the base address to be the next Gecko Code's address + {self.value:04X}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.PTR_GET_NEXT

    @property
    def value(self) -> int:
        return self.value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self.value = value & 0xFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | self.value
        return metadata.to_bytes(4, "big", signed=False) + b"\x00\x00\x00\x00"


class SetRepeat(GeckoCode):
    def __init__(self, repeat: int = 0, b: int = 0):
        self._repeat = repeat
        self.b = b

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) Store next code address and number of times to repeat in b{self.b}"

    def __len__(self) -> int:
        return 8

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.REPEAT_SET

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | self._repeat
        info = self.b
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class ExecuteRepeat(GeckoCode):
    def __init__(self, b: int = 0):
        self.b = b

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) If NNNN stored in b{self.b} is > 0, it is decreased by 1 and the code handler jumps to the next code address stored in b{self.b}"

    def __len__(self) -> int:
        return 8

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.REPEAT_EXEC

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24)
        info = self.b
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Return(GeckoCode):
    def __init__(self, flags: int = 0, b: int = 0):
        self.b = b
        self._flags = flags

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        if self._flags == 0:
            return f"({intType:02X}) If the code execution status is true, jump to the next code address stored in b{self.b} (NNNN in bP is not touched)"
        elif self._flags == 1:
            return f"({intType:02X}) If the code execution status is false, jump to the next code address stored in b{self.b} (NNNN in bP is not touched)"
        elif self._flags == 2:
            return f"({intType:02X}) Jump to the next code address stored in b{self.b} (NNNN in bP is not touched)"

    def __len__(self) -> int:
        return 8

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.RETURN

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._flags << 20)
        info = self.b
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Goto(GeckoCode):
    def __init__(self, flags: int = 0, lineOffset: int = 0):
        self._flags = flags
        self.offset = lineOffset

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        if self._flags == 0:
            return f"({intType:02X}) If the code execution status is true, jump to (next line of code + {self.offset} lines)"
        elif self._flags == 1:
            return f"({intType:02X}) If the code execution status is false, jump to (next line of code + {self.offset} lines)"
        elif self._flags == 2:
            return f"({intType:02X}) Jump to (next line of code + {self.offset} lines)"

    def __len__(self) -> int:
        return 8

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GOTO

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._flags << 20) | self.offset
        return metadata.to_bytes(4, "big", signed=False) + b"\x00\x00\x00\x00"


class Gosub(GeckoCode):
    def __init__(self, flags: int = 0, lineOffset: int = 0, register: int = 0):
        self._flags = flags
        self.offset = lineOffset
        self._register = register

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        if self._flags == 0:
            return f"({intType:02X}) If the code execution status is true, store the next code address in b{self._register} and jump to (next line of code + {self.offset} lines)"
        elif self._flags == 1:
            return f"({intType:02X}) If the code execution status is false, store the next code address in b{self._register} and jump to (next line of code + {self.offset} lines)"
        elif self._flags == 2:
            return f"({intType:02X}) Store the next code address in b{self._register} and jump to (next line of code + {self.offset} lines)"

    def __len__(self) -> int:
        return 8

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GOSUB

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._flags << 20) | self.offset
        info = self._register
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class GeckoRegisterSet(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x00:
            return f"({intType:02X}) Set Gecko Register {self._register} to the value 0x{self.value:08X}"
        elif flags == 0x01:
            return f"({intType:02X}) Set Gecko Register {self._register} to the value (0x{self.value:08X} + the {addrstr})"
        elif flags == 0x10:
            return f"({intType:02X}) Add the value 0x{self.value:08X} to Gecko Register {self._register}"
        elif flags == 0x11:
            return f"({intType:02X}) Add the value (0x{self.value:08X} + the {addrstr}) to Gecko Register {self._register}"
        return f"({intType:02X}) Invalid flag {flags}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_REG_SET

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class GeckoRegisterLoad(GeckoCode):
    def __init__(self, value: int, flags: int = 0, register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._flags = flags
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        flags = self._flags
        if flags == 0x00:
            return f"({intType:02X}) Set Gecko Register {self._register} to the byte at address 0x{self.value:08X}"
        elif flags == 0x10:
            return f"({intType:02X}) Set Gecko Register {self._register} to the short at address 0x{self.value:08X}"
        elif flags == 0x20:
            return f"({intType:02X}) Set Gecko Register {self._register} to the word at address 0x{self.value:08X}"
        elif flags == 0x01:
            return f"({intType:02X}) Set Gecko Register {self._register} to the byte at address (0x{self.value:08X} + the {addrstr})"
        elif flags == 0x11:
            return f"({intType:02X}) Set Gecko Register {self._register} to the short at address (0x{self.value:08X} + the {addrstr})"
        elif flags == 0x21:
            return f"({intType:02X}) Set Gecko Register {self._register} to the word at address (0x{self.value:08X} + the {addrstr})"
        return f"({intType:02X}) Invalid flag {flags}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_REG_LOAD

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class GeckoRegisterStore(GeckoCode):
    def __init__(self, value: int, repeat: int = 0, flags: int = 0,
                 register: int = 0, valueSize: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)

        self.value = value
        self._valueSize = valueSize
        self._flags = flags
        self._repeat = repeat
        self._register = register
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        valueType = ("byte", "short", "word")[self._valueSize]

        flags = self._flags
        if flags > 0x21:
            return f"({intType:02X}) Invalid flag {flags}"

        if self._repeat > 0:
            if flags & 0x01:
                return f"({intType:02X}) Store Gecko Register {self._register}'s {valueType} to [0x{self.value:08X} + the {addrstr}] {self._repeat + 1} times consecutively"
            else:
                return f"({intType:02X}) Store Gecko Register {self._register}'s {valueType} to [0x{self.value:08X}] {self._repeat + 1} times consecutively"
        else:
            if flags & 0x01:
                return f"({intType:02X}) Store Gecko Register {self._register}'s {valueType} to [0x{self.value:08X} + the {addrstr}]"
            else:
                return f"({intType:02X}) Store Gecko Register {self._register}'s {valueType} to [0x{self.value:08X}]"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_REG_STORE

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._flags << 12) | (
            self._repeat << 4) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class GeckoRegisterOperateI(GeckoCode):
    def __init__(self, value: int, opType: GeckoCode.ArithmeticType, flags: int = 0, register: int = 0):
        GeckoCode.assertRegister(register)

        self.value = value
        self._opType = opType
        self._register = register
        self._flags = flags

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        grAccessType = f"[Gecko Register {self._register}]" if (
            self._flags & 1) != 0 else f"Gecko Register {self._register}"
        valueAccessType = f"[{self.value:08X}]" if (
            self._flags & 0x2) != 0 else f"{self.value:08X}"
        opType = self._opType
        if opType == GeckoCode.ArithmeticType.ADD:
            return f"({intType:02X}) Add {valueAccessType} to {grAccessType}"
        elif opType == GeckoCode.ArithmeticType.MUL:
            return f"({intType:02X}) Multiply {grAccessType} by {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.OR:
            return f"({intType:02X}) OR {grAccessType} with {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.XOR:
            return f"({intType:02X}) XOR {grAccessType} with {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.SLW:
            return f"({intType:02X}) Shift {grAccessType} left by {valueAccessType} bits"
        elif opType == GeckoCode.ArithmeticType.SRW:
            return f"({intType:02X}) Shift {grAccessType} right by {valueAccessType} bits"
        elif opType == GeckoCode.ArithmeticType.ROL:
            return f"({intType:02X}) Rotate {grAccessType} left by {valueAccessType} bits"
        elif opType == GeckoCode.ArithmeticType.ASR:
            return f"({intType:02X}) Arithmetic shift {grAccessType} right by {valueAccessType} bits"
        elif opType == GeckoCode.ArithmeticType.FADDS:
            return f"({intType:02X}) Add {valueAccessType} to {grAccessType} as a float"
        elif opType == GeckoCode.ArithmeticType.FMULS:
            return f"({intType:02X}) Multiply {grAccessType} by {valueAccessType} as a float"
        return f"({intType:02X}) Invalid operation flag {opType}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_REG_OPERATE_I

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (int(self._opType) << 20) | (
            self._flags << 16) | self._register
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class GeckoRegisterOperate(GeckoCode):
    def __init__(self, otherRegister: int, opType: GeckoCode.ArithmeticType, flags: int = 0, register: int = 0):
        GeckoCode.assertRegister(register)
        GeckoCode.assertRegister(otherRegister)

        self._opType = opType
        self._register = register
        self._other = otherRegister
        self._flags = flags

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        grAccessType = f"[Gecko Register {self._register}]" if (
            self._flags & 1) != 0 else f"Gecko Register {self._register}"
        valueAccessType = f"[Gecko Register {self._other}]" if (
            self._flags & 0x2) != 0 else f"Gecko Register {self._other}"
        opType = self._opType
        if opType == GeckoCode.ArithmeticType.ADD:
            return f"({intType:02X}) Add {valueAccessType} to {grAccessType}"
        elif opType == GeckoCode.ArithmeticType.MUL:
            return f"({intType:02X}) Multiply {grAccessType} by {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.OR:
            return f"({intType:02X}) OR {grAccessType} with {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.XOR:
            return f"({intType:02X}) XOR {grAccessType} with {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.SLW:
            return f"({intType:02X}) Shift {grAccessType} left by {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.SRW:
            return f"({intType:02X}) Shift {grAccessType} right by {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.ROL:
            return f"({intType:02X}) Rotate {grAccessType} left by {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.ASR:
            return f"({intType:02X}) Arithmetic shift {grAccessType} right by {valueAccessType}"
        elif opType == GeckoCode.ArithmeticType.FADDS:
            return f"({intType:02X}) Add {valueAccessType} to {grAccessType} as a float"
        elif opType == GeckoCode.ArithmeticType.FMULS:
            return f"({intType:02X}) Multiply {grAccessType} by {valueAccessType} as a float"
        return f"({intType:02X}) Invalid operation flag {opType}"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_REG_OPERATE

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (int(self._opType) << 20) | (
            self._flags << 16) | self._register
        info = self._other
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class MemoryCopyTo(GeckoCode):
    def __init__(self, value: int, size: int, otherRegister: int = 0xF,
                 register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)
        GeckoCode.assertRegister(otherRegister)

        self.value = value
        self._size = size
        self._register = register
        self._other = otherRegister
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"

        if self._other == 0xF:
            return f"({intType:02X}) Copy 0x{self._size:04X} bytes from [Gecko Register {self._register}] to (the {addrstr} + 0x{self.value:08X})"
        else:
            return f"({intType:02X}) Copy 0x{self._size:04X} bytes from [Gecko Register {self._register}] to ([Gecko Register {self._other}] + 0x{self.value:08X})"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.MEMCPY_1

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._size << 8) | (
            self._register << 4) | self._other
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class MemoryCopyFrom(GeckoCode):
    def __init__(self, value: int, size: int, otherRegister: int = 0xF,
                 register: int = 0, isPointer: bool = False):
        GeckoCode.assertRegister(register)
        GeckoCode.assertRegister(otherRegister)

        self.value = value
        self._size = size
        self._register = register
        self._other = otherRegister
        self._isPointer = isPointer

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"

        if self._other == 0xF:
            return f"({intType:02X}) Copy 0x{self._size:04X} bytes from (the {addrstr} + 0x{self.value:08X}) to [Gecko Register {self._register}]"
        else:
            return f"({intType:02X}) Copy 0x{self._size:04X} bytes from ([Gecko Register {self._other}] + 0x{self.value:08X}) to [Gecko Register {self._register}]"

    def __len__(self) -> int:
        return 8

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.MEMCPY_2

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._size << 8) | (
            self._register << 4) | self._other
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class GeckoIfEqual16(GeckoCode):
    def __init__(self, address: int = 0, register: int = 0, otherRegister: int = 15,
                 isPointer: bool = False, endif: bool = False, mask: int = 0xFFFF):
        GeckoCode.assertRegister(register)
        GeckoCode.assertRegister(otherRegister)

        self._mask = mask
        self._address = address
        self._endif = endif
        self._register = register
        self._other = otherRegister
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        home = f"(Gecko Register {self._register} & ~0x{self._mask:04X})" if self._register != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        target = f"(Gecko Register {self._other} & ~0x{self._mask:04X})" if self._other != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If {home} is equal to {target}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_IF_EQ_16

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._other << 28) | (self._register << 24) | self._mask
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class GeckoIfNotEqual16(GeckoCode):
    def __init__(self, address: int = 0, register: int = 0, otherRegister: int = 15,
                 isPointer: bool = False, endif: bool = False, mask: int = 0xFFFF):
        GeckoCode.assertRegister(register)
        GeckoCode.assertRegister(otherRegister)

        self._mask = mask
        self._address = address
        self._endif = endif
        self._register = register
        self._other = otherRegister
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        home = f"(Gecko Register {self._register} & ~0x{self._mask:04X})" if self._register != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        target = f"(Gecko Register {self._other} & ~0x{self._mask:04X})" if self._other != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If {home} is not equal to {target}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_IF_NEQ_16

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._other << 28) | (self._register << 24) | self._mask
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class GeckoIfGreaterThan16(GeckoCode):
    def __init__(self, address: int = 0, register: int = 0, otherRegister: int = 15,
                 isPointer: bool = False, endif: bool = False, mask: int = 0xFFFF):
        GeckoCode.assertRegister(register)
        GeckoCode.assertRegister(otherRegister)

        self._mask = mask
        self._address = address
        self._endif = endif
        self._register = register
        self._other = otherRegister
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        home = f"(Gecko Register {self._register} & ~0x{self._mask:04X})" if self._register != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        target = f"(Gecko Register {self._other} & ~0x{self._mask:04X})" if self._other != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If {home} is greater than {target}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_IF_GT_16

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._other << 28) | (self._register << 24) | self._mask
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class GeckoIfLesserThan16(GeckoCode):
    def __init__(self, address: int = 0, register: int = 0, otherRegister: int = 15,
                 isPointer: bool = False, endif: bool = False, mask: int = 0xFFFF):
        GeckoCode.assertRegister(register)
        GeckoCode.assertRegister(otherRegister)

        self._mask = mask
        self._address = address
        self._endif = endif
        self._register = register
        self._other = otherRegister
        self._isPointer = isPointer
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        home = f"(Gecko Register {self._register} & ~0x{self._mask:04X})" if self._register != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        target = f"(Gecko Register {self._other} & ~0x{self._mask:04X})" if self._other != 0xF else f"the short at address (0x{self._address:08X} + the {addrstr})"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}If {home} is less than {target}:"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.GECKO_IF_LT_16

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFE) | (1 if self._endif else 0)
        info = (self._other << 28) | (self._register << 24) | self._mask
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class CounterIfEqual16(GeckoCode):
    def __init__(self, value: int, mask: int = 0xFFFF,
                 flags: int = 0, counter: int = 0):
        self.value = value
        self._mask = mask
        self._flags = flags
        self._counter = counter
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        ty = " (Resets counter if true)" if (self._flags &
                                             0x8) != 0 else " (Resets counter if false)"
        endif = "(Apply Endif) " if (self._flags & 0x1) != 0 else ""
        return f"({intType:02X}) {endif}If (0x{self.value:08X} & ~0x{self._mask:04X}) is equal to {self._counter}:{ty}"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.COUNTER_IF_EQ_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._counter << 4) | self._flags
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class CounterIfNotEqual16(GeckoCode):
    def __init__(self, value: int, mask: int = 0xFFFF,
                 flags: int = 0, counter: int = 0):
        self.value = value
        self._mask = mask
        self._flags = flags
        self._counter = counter
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        ty = " (Resets counter if true)" if (self._flags &
                                             0x8) != 0 else " (Resets counter if false)"
        endif = "(Apply Endif) " if (self._flags & 0x1) != 0 else ""
        return f"({intType:02X}) {endif}If (0x{self.value:08X} & ~0x{self._mask:04X}) is not equal to {self._counter}:{ty}"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.COUNTER_IF_NEQ_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._counter << 4) | self._flags
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class CounterIfGreaterThan16(GeckoCode):
    def __init__(self, value: int, mask: int = 0xFFFF,
                 flags: int = 0, counter: int = 0):
        self.value = value
        self._mask = mask
        self._flags = flags
        self._counter = counter
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        ty = " (Resets counter if true)" if (self._flags &
                                             0x8) != 0 else " (Resets counter if false)"
        endif = "(Apply Endif) " if (self._flags & 0x1) != 0 else ""
        return f"({intType:02X}) {endif}If (0x{self.value:08X} & ~0x{self._mask:04X}) is greater than {self._counter}:{ty}"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.COUNTER_IF_GT_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._counter << 4) | self._flags
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class CounterIfLesserThan16(GeckoCode):
    def __init__(self, value: int, mask: int = 0xFFFF,
                 flags: int = 0, counter: int = 0):
        self.value = value
        self._mask = mask
        self._flags = flags
        self._counter = counter
        self._children = []

    def __len__(self) -> int:
        return 8 + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        ty = " (Resets counter if true)" if (self._flags &
                                             0x8) != 0 else " (Resets counter if false)"
        endif = "(Apply Endif) " if (self._flags & 0x1) != 0 else ""
        return f"({intType:02X}) {endif}If (0x{self.value:08X} & ~0x{self._mask:04X}) is less than {self._counter}:{ty}"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.COUNTER_IF_LT_16

    @property
    def value(self) -> int:
        return self._value & 0xFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFF

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._counter << 4) | self._flags
        info = (self._mask << 16) | self.value
        body = b""
        for code in self:
            body += code.as_bytes()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + body


class AsmExecute(GeckoCode):
    def __init__(self, value: bytes):
        self.value = value

    def __len__(self) -> int:
        return 8 + len(self.value)

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) Execute the designated ASM once every pass"

    def __getitem__(self, index: int) -> bytes:
        return self.value[index]

    def __setitem__(self, index: int, value: bytes):
        if isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")
        self.value[index] = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.ASM_EXECUTE

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        self._value = value

    def virtual_length(self) -> int:
        return ((len(self) + 7) & -0x8) >> 3

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = intType << 24
        info = self.virtual_length()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + _align_bytes(self.value, alignment=8)


class AsmInsert(GeckoCode):
    def __init__(self, value: bytes, address: int = 0, isPointer: bool = False):
        self.value = value
        self._address = address
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 8 + len(self.value)

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        return f"({intType:02X}) Inject (b / b) the designated ASM at 0x{self._address:08X} + the {addrstr}"

    def __getitem__(self, index: int) -> bytes:
        return self.value[index]

    def __setitem__(self, index: int, value: bytes):
        if isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")
        self.value[index] = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.ASM_INSERT

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        self._value = value

    def virtual_length(self) -> int:
        return ((len(self) + 7) & -0x8) >> 3

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC)
        info = self.virtual_length()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + _align_bytes(self.value, alignment=8)


class AsmInsertLink(GeckoCode):
    def __init__(self, value: bytes, address: int = 0, isPointer: bool = False):
        self.value = value
        self._address = address
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 8 + len(self.value)

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        return f"({intType:02X}) Inject (bl / blr) the designated ASM at 0x{self._address:08X} + the {addrstr}"

    def __getitem__(self, index: int) -> bytes:
        return self.value[index]

    def __setitem__(self, index: int, value: bytes):
        if isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")
        self.value[index] = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.ASM_INSERT_L

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        self._value = value

    def virtual_length(self) -> int:
        return ((len(self) + 7) & -0x8) >> 3

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC)
        info = self.virtual_length()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + _align_bytes(self.value, alignment=8)


class WriteBranch(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, isPointer: bool = False):
        self.value = value
        self._address = address
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        return f"({intType:02X}) Write a translated branch at (0x{self._address:08X} + the {addrstr}) to 0x{self.value:08X}"

    def __getitem__(self, index: int) -> int:
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return self.value

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index != 0:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        self.value = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.WRITE_BRANCH

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def apply(self, dol: DolFile) -> bool:
        addr = self._address | 0x80000000
        if dol.is_mapped(addr):
            dol.seek(addr)
            dol.insert_branch(self.value, addr, lk=addr & 1)
            return True
        return False

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC)
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Switch(GeckoCode):
    def __init__(self):
        pass

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) Toggle the code execution status when reached (True <-> False)"

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.SWITCH

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        return b"\xCC\x00\x00\x00\x00\x00\x00\x00"


class AddressRangeCheck(GeckoCode):
    def __init__(self, value: int, isPointer: bool = False, endif: bool = False):
        self.value = value
        self._isPointer = isPointer
        self._endif = endif

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        endif = "(Apply Endif) " if self._endif else ""
        return f"({intType:02X}) {endif}Check if 0x{self[0]} <= {addrstr} < 0x{self[1]}"

    def __getitem__(self, index: int) -> int:
        if index not in {0, 1}:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return (self.value & (0xFFFF << (16 * (index ^ 1)))) << (16 * index)

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index not in {0, 1}:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        v = self.value
        v &= (0xFFFF << (16 * index))
        v |= (value & 0xFFFF) << (16 * (index ^ 1))
        self.value = v

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.ADDR_RANGE_CHECK

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) | (
            0x10 if self._isPointer else 0)
        metadata = (intType << 24) | self._endif
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Terminator(GeckoCode):
    def __init__(self, value: int):
        self.value = value

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        baStr = f" Set the base address to {self[0]:08X}." if self[0] != 0 else ""
        poStr = f" Set the pointer address to {self[1]:08X}." if self[1] != 0 else ""
        return f"({intType:02X}) Clear the code execution status.{baStr}{poStr}"

    def __getitem__(self, index: int) -> int:
        if index not in {0, 1}:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return (self.value & (0xFFFF << (16 * (index ^ 1)))) << (16 * index)

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index not in {0, 1}:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        v = self.value
        v &= (0xFFFF << (16 * index))
        v |= (value & 0xFFFF) << (16 * (index ^ 1))
        self.value = v

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.TERMINATOR

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = intType << 24
        info = self.value
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Endif(GeckoCode):
    def __init__(self, value: int, asElse: bool = False, numEndifs: int = 0):
        self.value = value
        self._asElse = asElse
        self._endifNum = numEndifs

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        baStr = f" Set the base address to {self[0]:08X}." if self[0] != 0 else ""
        poStr = f" Set the pointer address to {self[1]:08X}." if self[1] != 0 else ""
        elseStr = "Inverse the code execution status (else) " if self._asElse else ""
        endif = "(Apply Endif) " if self._endifNum == 1 else f"(Apply {self._endifNum} Endifs) "
        return f"({intType:02X}) {endif}{elseStr}{baStr}{poStr}"

    def __getitem__(self, index: int) -> int:
        if index not in {0, 1}:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        return (self.value & (0xFFFF << (16 * (index ^ 1)))) << (16 * index)

    def __setitem__(self, index: int, value: Union[int, bytes]):
        if index not in {0, 1}:
            raise IndexError(
                f"Index [{index}] is beyond the virtual code size")
        elif isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")

        v = self.value
        v &= (0xFFFF << (16 * index))
        v |= (value & 0xFFFF) << (16 * (index ^ 1))
        self.value = v

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.ENDIF

    @property
    def value(self) -> int:
        return self._value & 0xFFFFFFFF

    @value.setter
    def value(self, value: Union[int, bytes]):
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big", signed=False)
        self._value = value & 0xFFFFFFFF

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | (self._asElse << 20) | self._endifNum
        info = self.virtual_length()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False)


class Exit(GeckoCode):
    def __init__(self):
        pass

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) Flag the end of the codelist, the codehandler exits"

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.EXIT

    def virtual_length(self) -> int:
        return 1

    def as_bytes(self) -> bytes:
        return b"\xF0\x00\x00\x00\x00\x00\x00\x00"


class AsmInsertXOR(GeckoCode):
    def __init__(self, value: bytes, address: int = 0, isPointer: bool = False, mask: int = 0, xorCount: int = 0):
        self.value = value
        self._mask = mask
        self._xorCount = xorCount
        self._address = address
        self._isPointer = isPointer

    def __len__(self) -> int:
        return 8 + len(self.value)

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype) + (
            2 if self._isPointer else 0)
        addrstr = "pointer address" if self._isPointer else "base address"
        return f"({intType:02X}) Inject (b / b) the designated ASM at (0x{self._address:08X} + the {addrstr}) if the 16-bit value at the injection point (and {self._xorCount} additional values) XOR'ed equals 0x{self._mask:04X}"

    def __getitem__(self, index: int) -> bytes:
        return self.value[index]

    def __setitem__(self, index: int, value: bytes):
        if isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} to the data of {self.__class__.__name__}")
        self.value[index] = value

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.ASM_INSERT_XOR

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        self._value = value

    def virtual_length(self) -> int:
        return ((len(self) + 7) & -0x8) >> 3

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype) + (
            2 if self._isPointer else 0)
        metadata = (intType << 24) | (self._address & 0x1FFFFFC)
        info = (self._xorCount << 24) | (
            self._mask << 8) | self.virtual_length()
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + _align_bytes(self.value, alignment=8)


class BrainslugSearch(GeckoCode):
    def __init__(self, value: Union[int, bytes], address: int = 0, searchRange: Tuple[int, int] = [0x8000, 0x8180], numLines: int = 0):
        self.value = value
        self._address = address
        self._searchRange = searchRange
        self._count = numLines
        self._children = []

    def __len__(self) -> int:
        return 8 + len(self.value) + sum([len(c) for c in self])

    def __str__(self) -> str:
        intType = GeckoCode.type_to_int(self.codetype)
        return f"({intType:02X}) If the linear data search finds a match between addresses 0x{(self._searchRange[0] & 0xFFFF) << 16:08X} and 0x{(self._searchRange[1] & 0xFFFF) << 16:08X}, set the pointer address to the beginning of the match and run the encapsulated codes"

    def __getitem__(self, index: int) -> GeckoCode:
        return self._children[index]

    def __setitem__(self, index: int, value: GeckoCode):
        if not isinstance(value, GeckoCode):
            raise InvalidGeckoCodeError(
                f"Cannot assign {value.__class__.__name__} as a child of {self.__class__.__name__}")

        self._children[index] = value

    @property
    def children(self) -> List["GeckoCode"]:
        return self._children

    @property
    def codetype(self) -> GeckoCode.Type:
        return GeckoCode.Type.BRAINSLUG_SEARCH

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        self._value = value

    def add_child(self, child: "GeckoCode"):
        self._children.append(child)

    def remove_child(self, child: "GeckoCode"):
        self._children.remove(child)

    def virtual_length(self) -> int:
        return len(self.children) + 1

    def populate_from_bytes(self, f: IO):
        code = GeckoCode.bytes_to_geckocode(f)
        while code != Terminator:
            self.add_child(code)
            code = GeckoCode.bytes_to_geckocode(f)
        self.add_child(code)

    def as_bytes(self) -> bytes:
        intType = GeckoCode.type_to_int(self.codetype)
        metadata = (intType << 24) | self._count
        info = (self._searchRange[0] << 16) | self._searchRange[1]
        return metadata.to_bytes(4, "big", signed=False) + info.to_bytes(4, "big", signed=False) + _align_bytes(self.value, alignment=8)
