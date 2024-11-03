from sympy import totient
import math
from tqdm import tqdm

message = 'hello world!'

m_int = []
for char in message:
    print(f"char: {char} to int {ord(char)}")
    m_int.append(ord(char))

p=1009
q=3643
n = p * q
# 求n的欧拉函数
fai_n = (p-1) * (q-1)

result = {
    'e':[],
    'x':[]
}

for e in tqdm(range(2, fai_n)):
    # 判断e是否和fai_n互素
    if math.gcd(e, fai_n) == 1:
        x=0
        for m in m_int:
            if pow(m, e, n) == m:
                x+=1
        result['e'].append(e)
        result['x'].append(x)
min_x = min(result['x'])
min_e_values = [result['e'][i] for i in range(len(result['x'])) if result['x'][i] == min_x]

# 输出结果
sum_of_min_e = sum(min_e_values)
print(f"Minimum x: {min_x}")
# print(f"Corresponding e values: {min_e_values}")
print(f"Sum of corresponding e values: {sum_of_min_e}")
