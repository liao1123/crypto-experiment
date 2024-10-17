import base64
import os
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np

encode_message = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
cipher_text = base64.b64decode(encode_message)
random_key = np.random.bytes(16)
random_string = np.random.bytes(random.randint(0, 255))


def AES_ECB_encrypto(string):
    plaintext = random_string + string + cipher_text  # random-prefix || attacker-controlled || target-bytes
    plaintext = pad(plaintext, 16)
    aes = AES.new(random_key, AES.MODE_ECB)
    cipher = aes.encrypt(plaintext)

    return cipher


def crack_aes_ecb(encryption_oracle):
    key_size = 16
    # 寻找前缀长度
    padding_size = 0
    num_random_blocks = 0
    ciphertext_length = len(encryption_oracle(b''))
    prefix_length = len(os.path.commonprefix([encryption_oracle(b'AAAA'), encryption_oracle(b'')]))
    print("前缀长度：", prefix_length)

    # 查找随机块的数量
    for i in range(int(ciphertext_length / key_size)):
        if prefix_length < i * key_size:
            num_random_blocks = i
            break
    print("随机块数量：", num_random_blocks)

    # 查找所需的字节填充数
    base_ciphertext = encryption_oracle(b'')
    for i in range(1, key_size):
        new_ciphertext = encryption_oracle(b'A' * i)
        new_prefix_length = len(os.path.commonprefix([base_ciphertext, new_ciphertext]))
        if new_prefix_length > prefix_length:
            padding_size = i - 1
            break
        base_ciphertext = new_ciphertext
    print("需要填充的字节数：", padding_size)

    decrypted_bytes = b""
    ciphertext = encryption_oracle(decrypted_bytes)
    # 添加了填充，增加了一个块
    total_length = len(ciphertext) + key_size

    for i in range(key_size * num_random_blocks + 1, total_length + 1):
        padding_template = b'A' * (total_length - i + padding_size)
        cipher = encryption_oracle(padding_template)
        for j in range(256):
            input_text = padding_template + decrypted_bytes + j.to_bytes(1, "little")
            c = encryption_oracle(input_text)
            if c[total_length - key_size:total_length] == cipher[total_length - key_size:total_length]:
                decrypted_bytes += chr(j).encode()
                break
    return decrypted_bytes


if __name__ == '__main__':
    byte_text = crack_aes_ecb(AES_ECB_encrypto)
    print("\nDeciphered string:\n")
    print(byte_text.decode("utf-8").strip())
