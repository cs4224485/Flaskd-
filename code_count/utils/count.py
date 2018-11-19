# Author: harry.cai
# DATE: 2018/9/5
import os


def code_count(file_path):
    '''
    计算代码总行数
    :param file_path:
    :return: 总行数
    '''

    total = 0
    for base_dir, directory, file in os.walk(file_path):
        for item in file:
            file_path = os.path.join(base_dir, item)
            file_type = file_path.rsplit('.', maxsplit=1)
            if len(file_type) < 2:
                continue
            file_type = file_type[1]

            if file_type == 'py':
                code_lines = 0

                with open(file_path, 'rb') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith(b'#'):
                            continue
                        code_lines+=1
                total += code_lines
    return total
