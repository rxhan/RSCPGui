import logging
import math
from typing import Union

from py3rijndael import RijndaelCbc, ZeroPadding

logger = logging.getLogger(__name__)


class ParameterError(Exception):
    def __init__(self, message):
        logger.exception(message)


class RSCPEncryptDecrypt:
    KEY_SIZE: int = 32
    BLOCK_SIZE: int = 32

    def __init__(self, key: str):
        if len(key) > self.KEY_SIZE:
            raise ParameterError("Key must be <%d bytes" % self.KEY_SIZE)

        self.key = bytes(key.ljust(self.KEY_SIZE, '\xff'), encoding="latin_1")
        self.encrypt_init_vector = bytes('\xff' * self.BLOCK_SIZE, encoding="latin_1")
        self.decrypt_init_vector = bytes('\xff' * self.BLOCK_SIZE, encoding="latin_1")
        self.remaining_data = ''
        self.old_decrypt = ''

    def encrypt(self, plain_data: Union[str, bytes]) -> bytes:
        if isinstance(plain_data, str):
            plain_data = bytes(plain_data, encoding="latin_1")
        cbc = RijndaelCbc(key=self.key, iv=self.encrypt_init_vector, padding=ZeroPadding(self.BLOCK_SIZE),
                          block_size=self.BLOCK_SIZE)
        encrypted_data = cbc.encrypt(plain_data)
        self.encrypt_init_vector = encrypted_data[-self.BLOCK_SIZE:]
        return encrypted_data

    def decrypt(self, encrypted_data, previously_processed_data_index=None) -> bytes:
        if previously_processed_data_index is None:
            length = len(self.old_decrypt)
            if length % self.BLOCK_SIZE == 0:
                previously_processed_data_index = length
            else:
                previously_processed_data_index = int(self.BLOCK_SIZE * math.floor(length / self.BLOCK_SIZE))
        if previously_processed_data_index % self.BLOCK_SIZE != 0:
            previously_processed_data_index = int(
                self.BLOCK_SIZE * math.ceil(previously_processed_data_index / self.BLOCK_SIZE))
        remaining_data = self.old_decrypt[previously_processed_data_index:]
        if self.old_decrypt != '':
            self.decrypt_init_vector = self.old_decrypt[
                                       previously_processed_data_index - self.BLOCK_SIZE:previously_processed_data_index]
        self.old_decrypt = encrypted_data

        cbc = RijndaelCbc(key=self.key, iv=self.decrypt_init_vector, padding=ZeroPadding(self.BLOCK_SIZE),
                          block_size=self.BLOCK_SIZE)
        decrypt = cbc.decrypt(encrypted_data)
        return decrypt
