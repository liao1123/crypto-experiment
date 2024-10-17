import os
import random
from Crypto.Cipher import AES
from experiment2_2_1 import pkcs7_padding
import numpy as np


def AES_encryptor(text, iv, key):
    plaintext = (prepend_str.encode() + text + append_str.encode()).replace(b';', b'";"').replace(b'=', b'"="')
    padded_plaintext = pkcs7_padding(plaintext, len(key))
    aes = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = aes.encrypt(padded_plaintext)
    return ciphertext


def AES_decryptor(byte_string, iv, key):
    # 通过AES_CBC模式解密给定的密文并检查admin是否设置为true
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted_string = aes.decrypt(byte_string)
    return decrypted_string
    # if b";admin=true;" in decrypted_string:
    #     return True
    # else:
    #     return False


def cbc_bit_flipping(admin_param, key_size, encryptor_func):
    # 填充
    padding_bytes = 0
    num_random_blocks = 0  # 寻找前缀长度
    cipher_len = len(encryptor_func(b'', iv, random_aes_key))
    prefix_len = len(
        os.path.commonprefix([encryptor_func(b'AAAA', iv, random_aes_key), encryptor_func(b'', iv, random_aes_key)]))
    print("前缀长度：", prefix_len)

    # 查找随机块的数量
    for i in range(int(cipher_len / key_size)):
        if prefix_len < i * key_size:
            num_random_blocks = i
            break
    print("随机块数量：", num_random_blocks)

    # 查找所需的字节填充数
    base_ciphertext = encryptor_func(b'', iv, random_aes_key)
    for i in range(1, key_size):
        new_ciphertext = encryptor_func(b'A' * i, iv, random_aes_key)
        new_prefix_len = len(os.path.commonprefix([base_ciphertext, new_ciphertext]))
        if new_prefix_len > prefix_len:
            padding_bytes = i - 1
            break
        base_ciphertext = new_ciphertext
    print("需要填充的字节数量：", padding_bytes)

    # 翻转给定字符串的字节
    input_data = b'A' * padding_bytes + b"heytheremama"
    modified_string = b""
    ciphertext = encryptor_func(input_data, iv, random_aes_key)
    for i in range(len(admin_param)):
        modified_string += (ciphertext[i + (num_random_blocks - 1) * key_size] ^ (
                input_data[i + padding_bytes] ^ admin_param[i])).to_bytes(1, "big")

    modified_ciphertext = ciphertext[:(num_random_blocks - 1) * key_size] + modified_string + ciphertext[(
                                                                                                                 num_random_blocks - 1) * key_size + len(
        modified_string):]

    return modified_ciphertext


if __name__ == '__main__':
    prepend_str = "comment1=cooking%20MCs;userdata="
    append_str = ";comment2=%20like%20a%20pound%20of%20bacon"
    admin_param = b";admin=true;"

    aes_key_size = 16
    random_aes_key = np.random.bytes(aes_key_size)
    iv = np.random.bytes(aes_key_size)

    modified_cipher = cbc_bit_flipping(admin_param, aes_key_size, AES_encryptor)
    print(AES_decryptor(modified_cipher, iv, random_aes_key))
