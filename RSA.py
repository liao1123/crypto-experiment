import libnum
from Crypto.Util.number import getPrime, inverse

n_length = 100


# 生成大素数
def get_prime_number():
    return getPrime(n_length)


#计算逆元
def mod_inverse(e, fain):
    return inverse(e, fain)


#选择与fain互素的e
def choose_e(fain):
    # 一般选65537
    e = 65537
    return e


# 参数公钥和私钥
def para():
    p = get_prime_number()
    q = get_prime_number()
    n = p * q
    fain = (p - 1) * (q - 1)

    e = choose_e(fain)
    d = mod_inverse(e, fain)
    return (e, d, n)


# 加密
def encrypto(code, e, n):
    encrypted_message = pow(code, e, n)
    print('加密后结果：', encrypted_message)
    return encrypted_message


# 解密
def decrypto(code, d, n):
    decrypted_message = pow(code, d, n)
    print('解密后结果：', decrypted_message)
    return decrypted_message


if __name__ == '__main__':
    message = 'Hello, RSA!'
    print('原消息：', message)
    code = libnum.s2n(message)
    print('原消息编码：', code)
    e, d, n = para()
    encrypted_messsage = encrypto(code, e, n)
    decrypted_message = decrypto(encrypted_messsage, d, n)
    print("解码结果：", libnum.n2s(decrypted_message))
