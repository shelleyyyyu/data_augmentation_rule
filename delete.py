import random

def delete_word(sent):
    # 万一 您 不想 改善目前 的 情况 的话 ， 我们 会 向 法院 告贵 工厂 ， 也 要 跟 媒体 说 我们 住民 的 困扰 。
    tmp_list = list(sent.split(' '))
    if len(tmp_list) > 2:
        word_to_delete = random.sample(tmp_list, 1)[0]
        sent = sent.replace(' '+word_to_delete+' ', ' ')
        return ''.join(sent.split(' '))
    return None


def delete_char(sent):
    # 万一您不想改善目前的情况的话 ， 我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。
    tmp_list = list(sent)
    if len(tmp_list) > 2:
        char_to_delete = random.sample(tmp_list, 1)[0]
        sent = sent.replace(char_to_delete, '')
        return sent
    return None