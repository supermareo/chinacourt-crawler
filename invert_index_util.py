# coding=utf-8
import re
from collections import Counter
import jieba
import redis_util

from file_util import read_lines


def write_file(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def count_in_str(source, target=[]):
    # 去掉标点符号等
    line = re.sub("[.!//_,$&%^*()<>+\"'?@#-|:~{}]+|[——！\\\\，。=？、：“”‘’《》【】￥……（）]+", '', source)
    # 分词
    words = list(jieba.cut_for_search(line))
    # 仅选取要处理的单词
    if target is not None and len(target) > 0:
        words = list(filter(lambda s: s in target, words))
    # 统计单词数量
    counter = dict(Counter(words))
    return counter


if __name__ == '__main__':
    inverted_index = {
    }
    lines = read_lines('question_list.txt')
    lines = list(filter(lambda l: l.startswith('Q:'), lines))
    for line in lines:
        line = line.strip()[2:]
        one_line_data = count_in_str(line)
        for word, count in one_line_data.items():
            if not word in inverted_index:
                inverted_index[word] = {}
            inverted_index[word][line] = count

    # write to file
    lines = []
    for word_id, doc_id_freq_map in inverted_index.items():
        line = word_id
        for doc_id, freq in doc_id_freq_map.items():
            redis_util.set(word_id + ':' + doc_id, freq)
            line += '\t' + doc_id + '\t' + str(freq)
        lines.append(line)
    write_file('inversed_index.txt', lines)
