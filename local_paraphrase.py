import random

def exchange_word(sent):
    # 万一 您 不想 改善目前 的 情况 的话 ， 我们 会 向 法院 告贵 工厂 ， 也 要 跟 媒体 说 我们 住民 的 困扰 。
    tmp_list = list(sent.split(' '))
    word_index_to_exchange = random.sample([i for i in range(len(tmp_list)-2)], 1)[0]
    tmp_str = tmp_list[word_index_to_exchange]
    tmp_list[word_index_to_exchange] = tmp_list[word_index_to_exchange+1]
    tmp_list[word_index_to_exchange + 1] = tmp_str
    return ''.join(tmp_list)


def exchange_char(sent):
    tmp_list = list(sent)
    word_index_to_exchange = random.sample([i for i in range(len(tmp_list)-2)], 1)[0]
    tmp_str = tmp_list[word_index_to_exchange]
    tmp_list[word_index_to_exchange] = tmp_list[word_index_to_exchange+1]
    tmp_list[word_index_to_exchange + 1] = tmp_str
    return ''.join(tmp_list)