import logging

from typing import Union

logger = logging.getLogger(__name__)

MODBUS_READ_CMD: int = 0x3
MODBUS_WRITE_CMD: int = 0x6
MODBUS_WRITE_MULTI_CMD: int = 0x10


def _create_crc16_table() -> tuple:
    """Construct (modbus) CRC-16 table"""
    table = []
    for i in range(256):
        buffer = i << 1
        crc = 0
        for _ in range(8, 0, -1):
            buffer >>= 1
            if (buffer ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
        table.append(crc)
    return tuple(table)


_CRC_16_TABLE = _create_crc16_table()


def _modbus_checksum(data: Union[bytearray, bytes]) -> int:
    """
    Calculate modbus crc-16 checksum
    """
    crc = 0xFFFF
    for ch in data:
        crc = (crc >> 8) ^ _CRC_16_TABLE[(crc ^ ch) & 0xFF]
    return crc


def create_modbus_request(comm_addr: int, cmd: int, offset: int, value: int) -> bytes:
    """
    Create modbus request.
    data[0] is inverter address
    data[1] is modbus command
    data[2:3] is command offset parameter
    data[4:5] is command value parameter
    data[6:7] is crc-16 checksum
    """
    data: bytearray = bytearray(6)
    data[0] = comm_addr
    data[1] = cmd
    data[2] = (offset >> 8) & 0xFF
    data[3] = offset & 0xFF
    data[4] = (value >> 8) & 0xFF
    data[5] = value & 0xFF
    checksum = _modbus_checksum(data)
    data.append(checksum & 0xFF)
    data.append((checksum >> 8) & 0xFF)
    return bytes(data)


def create_modbus_multi_request(comm_addr: int, cmd: int, offset: int, values: bytes) -> bytes:
    """
    Create modbus (multi value) request.
    data[0] is inverter address
    data[1] is modbus command
    data[2:3] is command offset parameter
    data[4:5] is command value parameter
    data[6:7] is crc-16 checksum
    """
    data: bytearray = bytearray(7)
    data[0] = comm_addr
    data[1] = cmd
    data[2] = (offset >> 8) & 0xFF
    data[3] = offset & 0xFF
    data[4] = 0
    data[5] = len(values) // 2
    data[6] = len(values)
    data.extend(values)
    checksum = _modbus_checksum(data)
    data.append(checksum & 0xFF)
    data.append((checksum >> 8) & 0xFF)
    return bytes(data)


def validate_modbus_response(data: bytes, cmd: int, offset: int, value: int) -> bool:
    """
    Validate the modbus response.
    data[0:1] is header
    data[2] is source address
    data[3] is command return type
    data[4] is response payload length (for read commands)
    data[-2:] is crc-16 checksum
    """
    if len(data) <= 4:
        logger.debug(f'Response is too short.')
        return False
    if data[3] != cmd:
        logger.debug(f'Response returned command failure: {data[3]}, expected {cmd}.')
        return False
    if data[3] == MODBUS_READ_CMD:
        if data[4] != value * 2:
            logger.debug(f'Response has unexpected length: {data[4]}, expected {value * 2}.')
            return False
        expected_length = data[4] + 7
        if len(data) < expected_length:
            logger.debug(f'Response is too short: {len(data)}, expected {expected_length}.')
            return False
    elif data[3] in (MODBUS_WRITE_CMD, MODBUS_WRITE_MULTI_CMD):
        if len(data) < 10:
            logger.debug(f'Response has unexpected length: {len(data)}, expected {10}.')
            return False
        expected_length = 10
        response_offset = int.from_bytes(data[4:6], byteorder='big')
        if response_offset != offset:
            logger.debug(f'Response has wrong offset: {response_offset}, expected {offset}.')
            return False
        response_value = int.from_bytes(data[6:8], byteorder='big')
        if response_value != value:
            logger.debug(f'Response has wrong value: {response_value}, expected {value}.')
            return False
    else:
        expected_length = len(data)
    checksum_offset = expected_length - 2
    if _modbus_checksum(data[2:checksum_offset]) != ((data[checksum_offset + 1] << 8) + data[checksum_offset]):
        logger.debug(f'Response CRC-16 checksum does not match.')
        return False
    return True
