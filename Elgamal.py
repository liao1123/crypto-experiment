from random import randint, random
import random

import libnum
from Crypto.Util.number import getPrime, inverse

n_length = 256


# 生成大素数
def get_prime_number():
    return getPrime(n_length)


# 快速取模幂
def fastExpMod(a, e, m):
    a = a % m
    res = 1
    while e != 0:
        if e & 1:
            res = (res * a) % m
        e >>= 1  # 右移一位
        a = (a * a) % m
    return res


# 生成原根
def primitive_element(p):
    q = int((p - 1) / 2)
    while True:
        g = randint(2, p - 2)
        if fastExpMod(g, 2, p) != 1 and fastExpMod(g, q, p) != 1:
            return g


def para(p):
    g = primitive_element(p)
    x = random.randint(1, p - 1)
    y = pow(g, x, p)
    private_key, public_key = (p, g, x), (p, g, y)
    return private_key, public_key


# 加密
def encrypto(code, public_key):
    p, g, y = public_key
    k = random.randint(2, p - 2)
    C1 = fastExpMod(g, k, p)
    C2 = (code * fastExpMod(y, k, p)) % p
    encrypted_message = (C1, C2)
    return encrypted_message


# 解密
def decrypto(encrypted_message, private_key):
    p, g, x = private_key
    C1, C2 = encrypted_message
    V1 = fastExpMod(C1, x, p)
    V2 = inverse(V1, p)
    decrypted_message = (C2 * V2) % p
    print('解密后结果：', decrypted_message)
    return decrypted_message


if __name__ == '__main__':
    message = 'Hello, Elgamal!'
    print('原消息：', message)
    code = libnum.s2n(message)
    print('消息编码：', code)
    p = get_prime_number()
    private_key, public_key = para(p)
    encrypted_message = encrypto(code, public_key)
    print('加密信息：', encrypted_message)
    decrypted_message = decrypto(encrypted_message, private_key)
    print("解码信息：", libnum.n2s(decrypted_message))
