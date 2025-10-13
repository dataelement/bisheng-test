import math
def calculate_mem_usage_average(log_file_path, num):
    mem_usage_list = []
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        for i in range(1, len(lines), 2):  # 从第二行开始，每隔一行读取一次
            line = lines[i].split()
            mem_usage = float(line[3].split('GiB')[0])  # 提取内存使用量并转换为浮点数
            mem_usage_list.append(mem_usage)
    # 计算每份应该有多少元素，向上取整以确保所有元素都被分配
    chunk_size = math.ceil(len(mem_usage_list) / num)
    # 分割列表
    chunks = [mem_usage_list[i:i + chunk_size] for i in range(0, len(mem_usage_list), chunk_size)]
    # 确保分割成指定的份数
    if len(chunks) > num:
        last_chunk = chunks[-2] + chunks[-1]
        chunks = chunks[:-2] + [last_chunk]
    # 计算并打印每一份的平均内存使用量
    for idx, chunk in enumerate(chunks):
        average = sum(chunk) / len(chunk)
        print(f" day {idx + 1} average MEM USAGE: {average:.2f} GiB")
# Example usage:
calculate_mem_usage_average(r"C:\Users\35041\Desktop\docker.log", 7)