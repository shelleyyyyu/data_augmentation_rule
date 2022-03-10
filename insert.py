import random
import synonyms

def insert_word(sent):
    # 万一您不想改善目前的情况的话 ， 我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。
    tmp_list = list(sent.split(' '))
    if len(tmp_list) > 2:
        char_index_to_insert = random.sample([i for i in range(len(tmp_list))], 1)[0]
        incorrect_sent = tmp_list[:char_index_to_insert] + [tmp_list[char_index_to_insert]] + tmp_list[char_index_to_insert:]
        correct_sent = tmp_list[:char_index_to_insert] + ['-NONE-'] + tmp_list[char_index_to_insert:]
        return ''.join(incorrect_sent)#, ''.join(correct_sent)
    else:
        return None

def insert_char(sent):
    # 万一您不想改善目前的情况的话 ， 我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。
    tmp_list = list(sent)
    if len(tmp_list) > 2:
        char_index_to_insert = random.sample([i for i in range(len(tmp_list))], 1)[0]
        incorrect_sent = tmp_list[:char_index_to_insert] + [tmp_list[char_index_to_insert]] + tmp_list[char_index_to_insert:]
        correct_sent = tmp_list[:char_index_to_insert] + ['-NONE-'] + tmp_list[char_index_to_insert:]
        return ''.join(incorrect_sent)#, ''.join(correct_sent)
    return None

def insert_synonyms_word(sent):
    # 万一您不想改善目前的情况的话 ， 我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。
    recusive_cnt = 0
    tmp_list = list(sent.split(' '))
    while True and recusive_cnt <= 5:
        recusive_cnt += 1
        word_index_to_insert = random.sample([i for i in range(len(tmp_list))], 1)[0]
        word_to_insert = tmp_list[word_index_to_insert]
        synonyms_list = synonyms.nearby(word_to_insert, 10)[0]
        synonyms_score = synonyms.nearby(word_to_insert, 10)[1]
        synonyms_pass_index_list = [idx for idx, score in enumerate(synonyms_score) if score > 0.75 and score < 1.0]
        if len(synonyms_pass_index_list) > 1:
            synonyms_to_insert = synonyms_list[random.sample(synonyms_pass_index_list, 1)[0]]
            incorrect_sent = tmp_list[:word_index_to_insert] + [synonyms_to_insert] + tmp_list[word_index_to_insert:]
            correct_sent = tmp_list[:word_index_to_insert] + ['-NONE-'] + tmp_list[word_index_to_insert:]
            return ''.join(incorrect_sent)#, ''.join(correct_sent)

    return None
