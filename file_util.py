# coding=utf-8
def append_line(path, line):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def append_lines(path, lines):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(lines)


def read_lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()
