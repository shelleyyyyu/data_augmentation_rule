# coding='utf-8'

import sys
import pypinyin
import random
import char_sim
import os
import json

# G_CUR_DIR = os.path.abspath(os.path.dirname(__file__))
# G_DEP_DIR = G_CUR_DIR + "/../"
# sys.path.append(G_DEP_DIR)
# G_DEP_DIR = G_CUR_DIR + "/../bin/"
# sys.path.append(G_DEP_DIR)

# CHAR = "./dict/char_meta.txt"
char_sim = char_sim.CharFuncs("./dict/char_meta.txt")

def yinjie(word):
    s = ''
    for i in pypinyin.pinyin(word, heteronym=False, style=pypinyin.NORMAL):
        s = s + ''.join(i) + "\x01"
    return s


def get_pinyin_dict(line):
    pinyin_dict = {}
    pinyin_list = yinjie(line).split('\x01')
    clean_pinyin = []
    del_pinyin = []
    for pinyin in pinyin_list:
        if line.find(pinyin) != -1:
            line = line.replace(pinyin, '')
            del_pinyin.append(pinyin)
        elif pinyin not in del_pinyin:
            clean_pinyin.append(pinyin)
    list_line = list(line)
    if len(list_line) == len(clean_pinyin):
        for idx in range(len(list_line)):
            if list_line[idx] not in pinyin_dict:
                pinyin_dict.setdefault(list_line[idx], clean_pinyin[idx])
    return pinyin_dict


def get_candidate_words(origin, candidates):
    r_candidates = []
    sims = []
    for idx in range(len(candidates)):
        cnd = candidates[idx]
        sims.append((char_sim.comp_similarity(origin, cnd), candidates[idx]))
    sims.sort(key=lambda x: x[0], reverse=True)
    # print(sims)
    for i in range(0, min(5, len(sims))):
        r_candidates.append(sims[i][1])
    return r_candidates



def get_word_by_pron(original_word, yinjie_word, pron_dict, vocab_dict):
    replace_word = ''
    if yinjie_word in pron_dict:
        pron_list = pron_dict[yinjie_word]
        pron_list = [w for w in pron_list if w != original_word and w in vocab_dict]
        # 按一定相似度选择替换词汇
        # idf 打分 字形打分 选择top5随机
        candidate_words = get_candidate_words(original_word, pron_list)
        if len(candidate_words) > 0:
            replace_word = candidate_words[random.randint(0, len(candidate_words) - 1)]
    return replace_word



def generate_pronouce_sent(line, comma_dict, pron_dict, vocab_dict):
    cur_pinyin_dict = get_pinyin_dict(line)
    # 对原文中的每个字进行替换
    # for idx in range(len(line)):
    if len(line) > 0:
        char_flag = 1
        while char_flag:
            idx = random.randint(0, len(line) - 1)
            list_line = list(line)
            char = list_line[idx]
            if char not in comma_dict and char.isdigit() == False:
                char_flag = 0
        if char in cur_pinyin_dict:
            pron_char = get_word_by_pron(char, cur_pinyin_dict[char], pron_dict, vocab_dict)
            if len(pron_char) > 0:
                list_line[idx] = pron_char
                return '%s' % (''.join(list_line))
    return None
