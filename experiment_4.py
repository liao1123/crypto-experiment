import binascii
import math
import os
import random

import gmpy2


def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(a, b):
    gcd, x, y = extended_euclidean(a, b)
    return x % b

def mod_exp(a, b, c):
    result = 1
    base = a
    while b > 0:
        if b % 2 == 1:
            result = (result * base) % c
        b //= 2
        base = (base * base) % c
    return result

def deal_N(N_list):
    # 判断N是否有相同的————共模攻击
    for idx, data in enumerate(N_list):
        target = data
        qwe = [key for key, value in enumerate(N_list) if value == target]
        if len(qwe) != 1:
            print(f"模数N相同 : {qwe}")

    # 判断两个模数N是否有公因数————公因数分析
    for idx, data in enumerate(N_list):
        data = int(data, 16)
        for key, value in enumerate(N_list[idx + 1:], start=idx + 1):
            value = int(value, 16)
            gcd = extended_euclidean(data, value)[0]
            if gcd != 1:
                print(f"模数第 {idx} 和 第 {key} 存在公因数: {gcd}")

def deal_e(e_list):
    dirt = {}
    for idx, data in enumerate(e_list):
        data = int(data, 16)
        if data not in dirt:
            dirt[data] = [idx]
        else:
            dirt[data].append(idx)
    print(f"加密指数e相同 : {dirt}")

def Common_Modulus_attack(N_list, e_list, c_list):
    N = int(N_list[0], 16)
    e1, e2 = int(e_list[0], 16), int(e_list[4], 16)
    c1, c2 = int(c_list[0], 16), int(c_list[4], 16)

    gcd, s1, s2 = extended_euclidean(e1, e2)

    # 求模反元素
    if s1 < 0:
        s1 = - s1
        c1 = gmpy2.invert(c1, N)
    elif s2 < 0:
        s2 = - s2
        c2 = gmpy2.invert(c2, N)

    m = (mod_exp(c1, s1, N) * mod_exp(c2, s2, N)) % N

    result = binascii.a2b_hex(hex(m)[2:])[-8:]
    print(f"Frame 0 result : {result}")
    print(f"Frame 4 result : {result}")


def gcd_attack(N_list, e_list, c_list):
    N1, N2 = int(N_list[1], 16), int(N_list[18], 16)
    e1, e2 = int(e_list[1], 16), int(e_list[18], 16)
    c1, c2 = int(c_list[1], 16), int(c_list[18], 16)

    # 求N1 N2的最大公因数
    gcd, s1, s2 = extended_euclidean(N1, N2)
    p1, p2 = gcd, gcd
    q1 = N1 // p1
    q2 = N2 // p2

    fai_n_1 = (p1-1) * (q1-1)
    fai_n_2 = (p2 - 1) * (q2 - 1)

    d1 = mod_inverse(e1, fai_n_1)
    d2 = mod_inverse(e2, fai_n_2)

    m1 = mod_exp(c1, d1, N1)
    m2 = mod_exp(c2, d2, N2)

    m1 = binascii.a2b_hex(hex(m1)[2:])[-8:]
    m2 = binascii.a2b_hex(hex(m2)[2:])[-8:]

    print(f"Frame 1 result: {m1}")
    print(f"Frame 18 result: {m2}")

def chinese_remainder_theorem(items):
    N = 1
    for a, n in items:
        N *= n
        result = 0
    for a, n in items:
        m = N//n
        d, r, s = extended_euclidean(n, m)
        if d != 1:
            N = N//n
            continue
        result += a*s*m
    return result % N, N

def low_e_broadcast_attack_5(N_list, e_list, c_list):
    iiid = [3, 8, 12, 16, 20]
    items = []
    for idx in iiid:
        N = int(N_list[idx], 16)
        c = int(c_list[idx], 16)
        items.append((c, N))

    mess, _ = chinese_remainder_theorem(items)

    # 直接对mess开五次方根
    result = gmpy2.iroot(gmpy2.mpz(mess), 5)
    result = binascii.a2b_hex(hex(result[0])[2:])[-8:]

    print(f"Frame 3 result: {result}")
    print(f"Frame 8 result: {result}")
    print(f"Frame 12 result: {result}")
    print(f"Frame 16 result: {result}")
    print(f"Frame 20 result: {result}")

def low_e_broadcast_attack_3(N_list, e_list, c_list):
    iiid = [7, 11, 15]
    items = []
    for idx in iiid:
        N = int(N_list[idx], 16)
        c = int(c_list[idx], 16)
        items.append((c, N))

    mess, _ = chinese_remainder_theorem(items)

    # 直接对mess开三次方根
    result = gmpy2.iroot(gmpy2.mpz(mess), 3)
    result = binascii.a2b_hex(hex(result[0])[2:])[-8:]

    print(f"Frame 7 result: {result}")
    print(f"Frame 11 result: {result}")
    print(f"Frame 15 result: {result}")

def low_e_3(N_list, e_list, c_list, K_max=100):
    iiid = [7, 11, 15]
    for idx in iiid:
        for k in range(K_max+1):
            N = int(N_list[idx], 16)
            c = int(c_list[idx], 16)

            # 直接对mess开三次方根
            mess = c + k*N
            result = gmpy2.iroot(gmpy2.mpz(mess), 3)
            result = binascii.a2b_hex(hex(result[0])[2:])[-8:]
            print(f"Frame {idx} k={k} result: {result}")

def fermat_factorization(N, max_iter=2**14):
    sqrt_n = gmpy2.isqrt(N) + 1  # 初始值 sqrt(N) + 1
    for i in range(max_iter):
        x = sqrt_n + i
        delta = x**2 - N
        if gmpy2.is_square(delta):  # 判断 delta 是否为完全平方数
            y = gmpy2.isqrt(delta)
            p = x + y
            q = x - y
            return p
    return None

def fermat_fenjie(N_list, e_list, c_list):
    iiiid = [10]
    for idx in iiiid:
        N = int(N_list[idx], 16)
        e = int(e_list[idx], 16)
        c = int(c_list[idx], 16)

        p = fermat_factorization(N)
        if p is None:
            continue
        q = N // p
        fai_n = (p-1) * (q-1)
        d = mod_inverse(e, fai_n)

        m = mod_exp(c, d, N)
        result = binascii.a2b_hex(hex(m)[2:])[-8:]
        print(f"Frame {idx} result: {result}")



def pollard_p_1(n, B=2**20):
    a = 2
    for i in range(2, B + 1):
        a = mod_exp(a, i, n)  # a = (a^i) % n
        d = gmpy2.gcd(a - 1, n)  # 求 gcd(a-1, n)
        if 1 < d < n:
            return d
    return None


def pollard_fenjie(N_list, e_list, c_list):
    iiid = [2, 6, 19]
    for idx in iiid:
        N = int(N_list[idx], 16)
        c = int(c_list[idx], 16)
        e = int(e_list[idx], 16)

        p = pollard_p_1(N)
        if p is None:
            continue
        q = N // p
        fai_n = (p - 1) * (q - 1)
        d = mod_inverse(e, fai_n)

        m = mod_exp(c, d, N)
        result = binascii.a2b_hex(hex(m)[2:])[-8:]
        print(f"Frame {idx} result: {result}")



if __name__ == '__main__':
    path = "frame_experiment"
    # 都为256位的16进制
    N_list, e_list, c_list = [], [], []

    for data in range(21):
        frame_path = os.path.join(path, f"Frame{data}")

        with open(frame_path, 'rb') as frame_file:
            frame = frame_file.readline()
            length = len(frame)
            N = frame[:length // 3]
            e = frame[length // 3:(2 * length) // 3]
            c = frame[2 * length // 3:]
            N_list.append(N)
            e_list.append(e)
            c_list.append(c)
    # 模数N相同 : [0, 4]
    # 模数第 1 和 第 18 存在公因数: 7273268163465293471933643674908027120929096536045429682300347130226398442391418956862476173798834057392247872274441320512158525416407044516675402521694747
    deal_N(N_list)
    # 比较大的：[0，4],
    # 65537: [1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 19],
    # 5: [3, 8, 12, 16, 20],
    # 3: [7, 11, 15]}
    deal_e(e_list)

    # 对frame 0 4 应用共模攻击
    Common_Modulus_attack(N_list, e_list, c_list)

    # 对frame 1 18 应用公因数攻击
    gcd_attack(N_list, e_list, c_list)

    # # 对frame 3 8 12 16 20 应用低加密指数广播攻击
    low_e_broadcast_attack_5(N_list, e_list, c_list)

    # # 对frame 7 11 15应用低加密指数k爆破攻击
    # # 失败！！！低加密指数k爆破攻击
    # low_e_3(N_list, e_list, c_list)
    # # 失败！！！ 低加密指数广播攻击也失败
    # low_e_broadcast_attack_3(N_list, e_list, c_list)


    # # 对frame 10 应用fermat分解p、q相差比较近的n
    fermat_fenjie(N_list, e_list, c_list)

    # 对frame 2 6 19 应用pollard p-1分解p、q相差比较远的n
    pollard_fenjie(N_list, e_list, c_list)

    #




