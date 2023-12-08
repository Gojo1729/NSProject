import json
import math
from typing import List
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util import strxor
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor as xordata
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Decryption:
    def hash_256(self, message):
        sha_256 = SHA256.new(message).digest()
        return sha_256

    def decrypt(self, message: bytes, Key: bytes, IV: bytes):
        b = self.hash_256(Key + IV)
        decrypted_blocks = []

        batch_size = 32
        msg_len = len(message)
        n_batches = math.ceil(msg_len / batch_size)
        # print(f"{n_batches=}")
        encrypted_blocks = b""
        b = self.hash_256(Key + IV)
        concatenated_decrypted_message = b""

        for batch_number in range(n_batches):
            batch_start = batch_number * batch_size
            batch_end = batch_start + batch_size
            enc_block = encrypted_blocks[batch_start:batch_end]
            # print(f"Batch size {len(msg_block)=}")
            decrypted_block = xordata(b, enc_block)
            decrypted_blocks.append(decrypted_block)
            b = self.hash_256(Key + enc_block)

        unpaded_dmsg = unpad(concatenated_decrypted_message, 32)
        decrypted_message = unpaded_dmsg.decode()
        decrypted_json = dict(json.loads(decrypted_message))

        return decrypted_json
