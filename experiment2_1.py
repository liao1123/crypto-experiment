import base64
from Crypto.Cipher import AES
import binascii
from hashlib import sha1
import codecs


def calculate_yan(num):
    weight = [7, 3, 1]
    sum = 0
    for idx, value in enumerate(num):
        sum += weight[idx % 3] * value
    return sum % 10


def key_Check(x):
    k_list = []
    a = bin(int(x, 16))[2:]
    for i in range(0, len(a), 8):
        if (a[i:i + 7].count("1")) % 2 == 0:
            k_list.append(a[i:i + 7])
            k_list.append('1')
        else:
            k_list.append(a[i:i + 7])
            k_list.append('0')
    k = hex(int(''.join(k_list), 2))
    return k


def main():
    encode_message = "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI"
    cipher_text = base64.b64decode(encode_message)
    # print(f"cipher text: {cipher_text}")
    IV = '0' * 32

    # 计算校验位 根据规则
    num = [1, 1, 1, 1, 1, 6]
    yan_value = calculate_yan(num)
    print(f"检验位值为：{yan_value}")

    mrz_data = "12345678<81110182111116" + str(yan_value)
    print(f"mrz_data: {mrz_data}")
    sha_info = sha1(mrz_data.encode()).hexdigest()
    print(sha_info)
    key_seed = sha_info[:32]
    data = key_seed + '00000001'
    key_hash = sha1(codecs.decode(data, "hex")).hexdigest()

    ka = key_hash[:16]
    kb = key_hash[16:32]

    ka = key_Check(ka)
    kb = key_Check(kb)
    key_finally = ka[2:] + kb[2:]

    # 输入key IV为字节类型
    aes = AES.new(binascii.unhexlify(key_finally), AES.MODE_CBC, binascii.unhexlify(IV))
    plaint_text = aes.decrypt(cipher_text)
    print(f"plaint text: {plaint_text}")


if __name__ == '__main__':
    main()
