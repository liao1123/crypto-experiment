def pkcs7_padding(data: bytes, block_size: int) -> bytes:
    data_length = len(data)
    padding_length = block_size - (data_length % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

# pkcs7 缺几位补几个几 比如这个例题缺4个字节，补4个04
# 示例
# message = b"YELLOW SUBMARINE"
# block_size = 20
# padded_message = pkcs7_padding(message, block_size)
#
# print(padded_message)
