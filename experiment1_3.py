import base64
import string


# 计算汉明距离
def calculate_hamming_distance(a, b):
    distance = 0
    for byte_a, byte_b in zip(a, b):
        res = byte_a ^ byte_b
        distance += bin(res).count('1')
    return distance


# 猜测密钥长度
def get_key_size(cipher_bytes):
    key_sizes = []
    for key_size in range(2, 41):
        blocks = [cipher_bytes[i:i + key_size] for i in range(0, len(cipher_bytes), key_size)]
        distances = []
        for i in range(len(blocks) - 1):
            block1 = blocks[i]
            block2 = blocks[i + 1]
            distance = calculate_hamming_distance(block1, block2) / key_size
            distances.append(distance)
        avg_distance = sum(distances) / len(distances)
        key_sizes.append({'key_size': key_size, 'avg_distance': avg_distance})
    # 选择具有最小平均归一化汉明距离的密钥长度
    chosen_key_size = min(key_sizes, key=lambda x: x['avg_distance'])
    return chosen_key_size['key_size']


# 英文频率评分
def english_scoring(text):
    letter_frequency = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .15000
    }
    return sum([letter_frequency.get(chr(byte), 0) for byte in text.lower()])


# 单字节 XOR 解密
def single_xor(ciphertext, single_char):
    return bytes([byte ^ single_char for byte in ciphertext])


# 破解单字节 XOR 密文
def decrypt_single_byte_xor(ciphertext):
    scores = []
    for single_char in range(256):
        decrypted_text = single_xor(ciphertext, single_char)
        score = english_scoring(decrypted_text)
        scores.append({'char': single_char, 'decrypted_text': decrypted_text, 'score': score})
    return max(scores, key=lambda x: x['score'])


# 使用重复密钥 XOR 解密
def repeating_key_xor(ciphertext, key):
    return bytes([ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))])


# 破解重复密钥 XOR 加密的密文
def break_repeating_key_xor(ciphertext):
    key_size = get_key_size(ciphertext)
    print(f"Chosen key size: {key_size}")

    blocks = [ciphertext[i:i + key_size] for i in range(0, len(ciphertext), key_size)]
    key = b''

    for i in range(key_size):
        column = bytes([block[i] for block in blocks if i < len(block)])
        result = decrypt_single_byte_xor(column)
        key += bytes([result['char']])

    decrypted_message = repeating_key_xor(ciphertext, key)
    return decrypted_message, key


if __name__ == '__main__':
    with open('experiment1_3_txt.txt') as file:
        ciphertext = file.read()
        cipher_bytes = base64.b64decode(ciphertext)
    decrypted_message, key = break_repeating_key_xor(cipher_bytes)
    print("Decrypted message:", decrypted_message.decode())
    print("Key:", key.decode())
