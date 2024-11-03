import math
from tqdm import tqdm


def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean(b % a, a)
        return gcd, y - (b // a) * x, x


def mod_inverse(e, phi_n):
    gcd, x, y = extended_euclidean(e, phi_n)
    if gcd != 1:
        return None  # 或者抛出异常，因为不存在逆元
    else:
        return x % phi_n  # 确保结果是正的


message = 'hello world!'
print(f"明文：{message}")
m_int = []
for char in message:
    print(f"char: {char} to int {ord(char)}")
    m_int.append(ord(char))

p = 1009
q = 3643
n = p * q
# 求n的欧拉函数
fai_n = (p - 1) * (q - 1)

# 随机选一个e和fai_n互素
for e in range(2, fai_n):
    if math.gcd(e, fai_n) == 1:
        print(f"choose e value : {e}")
        break

# 计算d
d = mod_inverse(e, fai_n)
print(f"d value: {d}")

# 加密
cipher_text = []
for data in tqdm(m_int):
    e_data = pow(data, e, n)
    cipher_text.append(e_data)

# 打印加密后的文本
print("加密后的文本：", cipher_text)

# 解密
decrypted_text = []
for data in cipher_text:
    d_data = pow(data, d, n)
    decrypted_text.append(chr(d_data))

# 打印解密后的文本
print(f"解密后的文本：{''.join(decrypted_text)}")
