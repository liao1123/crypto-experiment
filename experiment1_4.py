import hashlib
import itertools
import datetime

# 记录开始时间
start_time = datetime.datetime.now()
target_hash = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"

# 基础字符集和其替代组合
base_string = "QqWw%58(=0Ii*+nN"
combinations = [
    ['Q', 'q'], ['W', 'w'], ['%', '5'], ['8', '('],
    ['=', '0'], ['I', 'i'], ['*', '+'], ['n', 'N']
]


# 计算字符串的 SHA-1 哈希值
def compute_sha1(input_string):
    encoded_string = input_string.encode('utf-8')
    sha1_hash = hashlib.sha1(encoded_string)
    return sha1_hash.hexdigest()


# 生成所有可能的组合
all_combinations = itertools.product(*combinations)

for combination in all_combinations:
    combined_string = "".join(combination)

    for permutation in itertools.permutations(combined_string, 8):
        permuted_string = "".join(permutation)
        hash_result = compute_sha1(permuted_string)

        # 如果哈希匹配，输出匹配结果并结束
        if hash_result == target_hash:
            print(f"The matching string is: {permuted_string}")
            end_time = datetime.datetime.now()
            elapsed_time = (end_time - start_time).seconds
            print(f"The running time is: {elapsed_time} seconds")
            break
    else:
        continue
    break
