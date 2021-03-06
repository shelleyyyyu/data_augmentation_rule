import argparse
import jieba
import delete
import insert
import substitution
import pronouce
import local_paraphrase
import random
import json
# Reference 同義詞開源項目
# https://github.com/chatopera/Synonyms

def parse_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--augment_file', type=str)
    parser.add_argument('--augment_count', type=int, default=10)
    parser.add_argument('--save_file', type=str)
    parser.add_argument('--one_to_many', action='store_true')
    return parser.parse_args()

def get_comma_dict(filename):
    comma_dict = {}
    for line in open(filename, 'r', encoding='utf-8'):
        line = line.strip('\n')
        if line not in comma_dict:
            comma_dict.setdefault(line, 1)
    return comma_dict

def get_pron_dict(filename):
    pron_dict = {}
    for line in open(filename, 'r', encoding='utf-8'):
        line = line.strip('\n')
        fields = line.split('\t')
        if len(fields) == 2:
            pron_dict.setdefault(fields[0], fields[1].split(','))
    return pron_dict

def get_vocab_dict(filename):
    vocab_dict = {}
    for line in open(filename, 'r', encoding='utf-8'):
        line = line.strip('\n')
        if line not in vocab_dict:
            vocab_dict.setdefault(line, 1)
    return vocab_dict

def main():
    args = parse_config()
    to_augment_dlist = {}
    origin_dlist = []
    with open(args.augment_file, 'r', encoding='utf-8') as file:
        raw_data = file.readlines()
        # Special Handle for each dataset
        if 'SIGHAN' in args.augment_file:
            for d in raw_data:
                incorrect = d.strip().split('\t')[0]
                correct = d.strip().split('\t')[1]
                origin_dlist.append(incorrect+'\t'+correct+'\n')
                if correct not in to_augment_dlist:
                    tokenized_sent = ' '.join(jieba.cut(correct))
                    to_augment_dlist[correct] = tokenized_sent

        if 'babymom' in args.augment_file:
            for d in raw_data:
                incorrect = d.strip().split('\t')[1]
                correct = d.strip().split('\t')[2]
                origin_dlist.append(incorrect+'\t'+correct+'\n')
                if correct not in to_augment_dlist:
                    tokenized_sent = ' '.join(jieba.cut(correct))
                    to_augment_dlist[correct] = tokenized_sent

        if 'OCR' in args.augment_file:
            for d in raw_data:
                incorrect = d.strip().split('\t')[1]
                correct = d.strip().split('\t')[2]
                origin_dlist.append(incorrect+'\t'+correct+'\n')
                if correct not in to_augment_dlist:
                    tokenized_sent = ' '.join(jieba.cut(correct))
                    to_augment_dlist[correct] = tokenized_sent

        if 'zh_full_merge_data' in args.augment_file:
            for d in raw_data:
                if len(d.strip().split('\t')) == 2:
                    incorrect = d.strip().split('\t')[0]
                    correct = d.strip().split('\t')[1]
                    origin_dlist.append(incorrect+'\t'+correct+'\n')
                    if correct not in to_augment_dlist:
                        tokenized_sent = ' '.join(jieba.cut(correct))
                        to_augment_dlist[correct] = tokenized_sent


    comma_dict = get_comma_dict('./dict/comma_words.txt')
    pron_dict = get_pron_dict('./dict/prononcation.txt')
    vocab_dict = get_vocab_dict('./dict/vocab.txt')

    char_pronounce_dict = {}
    char_shape_dict = {}
    # Confusion_Net

    with open('confusion_set/Bakeoff2013_CharacterSet_SimilarPronunciation.txt', 'r', encoding='utf-8') as file:
        raw_pronounce_data = file.readlines()
        for d in raw_pronounce_data[1:]:
            zh_char = d.split('\t')[0]
            sameyin_samediao = d.split('\t')[1]
            sameyin_yidiao = d.split('\t')[2]
            jingyin_samediao = d.split('\t')[3]
            jingyin_yidiao = d.split('\t')[4]
            # won't consider this
            sameyin_samestrokenum = d.split('\t')[5]
            tmp_dict = {}
            tmp_dict['sameyin_samediao'] = list(sameyin_samediao)
            tmp_dict['sameyin_yidiao'] = list(sameyin_yidiao)
            tmp_dict['jingyin_samediao'] = list(jingyin_samediao)
            tmp_dict['jingyin_yidiao'] = list(jingyin_yidiao)
            char_pronounce_dict[zh_char] = tmp_dict

    with open('confusion_set/Bakeoff2013_CharacterSet_SimilarShape.txt', 'r', encoding='utf-8') as file:
        raw_shape_data = file.readlines()
        for d in raw_shape_data:
            char = d.strip().split(',')[0]
            sim_shape_char = list(d.strip().split(',')[1])
            char_shape_dict[char] = sim_shape_char

    population = ['w_del', 'w_ins_same', 'w_ins_syn', 'w_sub_syn', 'w_paraph', 'c_del',
                  'c_ins', 'c_sub_pronounce', 'c_sub_shape', 'c_paraph']
    if 'OCR' in args.save_file or 'ocr' in args.save_file:
        # OCR
        weight = [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0]
    elif 'SIGHAN' in args.save_file or 'sighan' in args.save_file:
        # SIGHAN
        weight = [0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0]
    elif 'BabyMom' in args.save_file or 'babymom' in args.save_file:
        # BabyMom
        weight = [0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0]
    else:
        # NLPCC
        weight = [0.11, 0.065, 0.065, 0.235, 0.025, 0.11, 0.13, 0.1175, 0.1175, 0.025]

    if args.one_to_many:
        with open(args.save_file, 'w', encoding='utf=8') as w_file:
            for key, value in to_augment_dlist.items():
                for i in range(args.augment_count):
                    type = random.choices(population, weight)[0]
                    origin = ''.join(value.split(' '))
                    augment_sent = None
                    if type == 'w_del':
                        augment_sent = delete.delete_word(value)
                    if type == 'w_ins_same':
                        augment_sent = insert.insert_word(value)
                    if type == 'w_ins_syn':
                        augment_sent = insert.insert_synonyms_word(value)
                    if type == 'w_sub_syn':
                        augment_sent = substitution.substitute_synonym_word(value)
                    if type == 'w_paraph':
                        augment_sent = local_paraphrase.exchange_word(value)
                    if type == 'c_del':
                        augment_sent = delete.delete_char(key)
                    if type == 'c_ins':
                        augment_sent = insert.insert_char(key)
                    if type == 'c_sub_pronounce':
                        # augment_sent = substitution.substitute_homonym_char(key, char_pronounce_dict)
                        augment_sent = pronouce.generate_pronouce_sent(key, comma_dict, pron_dict, vocab_dict)
                    if type == 'c_sub_shape':
                        augment_sent = substitution.substitute_shape_char(key, char_shape_dict)
                    if type == 'c_paraph':
                        augment_sent = local_paraphrase.exchange_char(key)
                    if augment_sent and augment_sent != '' and augment_sent != ' ':
                        w_file.write(augment_sent + '\t' + key + '\n')
            for data in origin_dlist:
                w_file.write(data)
    else:
        with open(args.save_file, 'w', encoding='utf=8') as w_file:
            for i in range(args.augment_count):
                #for key, value in to_augment_dlist.items():
                if i % 10000 == 0:
                    print('Current Augment Count: %d' %i)
                to_augment_sent = random.sample(to_augment_dlist.keys(), 1)[0]
                key = to_augment_sent
                value = to_augment_dlist[to_augment_sent]
                type = random.choices(population, weight)[0]
                origin = ''.join(value.split(' '))
                augment_sent = None
                if type == 'w_del':
                    augment_sent = delete.delete_word(value)
                if type == 'w_ins_same':
                    augment_sent = insert.insert_word(value)
                if type == 'w_ins_syn':
                    augment_sent = insert.insert_synonyms_word(value)
                if type == 'w_sub_syn':
                    augment_sent = substitution.substitute_synonym_word(value)
                if type == 'w_paraph':
                    augment_sent = local_paraphrase.exchange_word(value)
                if type == 'c_del':
                    augment_sent = delete.delete_char(key)
                if type == 'c_ins':
                    augment_sent = insert.insert_char(key)
                if type == 'c_sub_pronounce':
                    # augment_sent = substitution.substitute_homonym_char(key, char_pronounce_dict)
                    augment_sent = pronouce.generate_pronouce_sent(key, comma_dict, pron_dict, vocab_dict)
                if type == 'c_sub_shape':
                    augment_sent = substitution.substitute_shape_char(key, char_shape_dict)
                if type == 'c_paraph':
                    augment_sent = local_paraphrase.exchange_char(key)
                if augment_sent and augment_sent != '' and augment_sent != ' ':
                    w_file.write(augment_sent + '\t' + key + '\n')
            for data in origin_dlist:
                w_file.write(data)

    # # 構建INSERT類型糾錯 1147+13507
    # augment_sent = delete.delete_word('万一 您 不想 改善目前 的 情况 的话 ， 我们 会 向 法院 告贵 工厂 ， 也 要 跟 媒体 说 我们 住民 的 困扰 。')
    # print(augment_sent)
    # augment_sent = delete.delete_char('万一您不想改善目前的情况的话，我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。')
    # print(augment_sent)
    #
    # # 構建DELETE類型糾錯 911+11325
    # augment_sent = insert.insert_word('万一 您 不想 改善目前 的 情况 的话 ， 我们 会 向 法院 告贵 工厂 ， 也 要 跟 媒体 说 我们 住民 的 困扰 。')
    # print(augment_sent)
    # augment_sent = insert.insert_char('万一您不想改善目前的情况的话，我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。')
    # print(augment_sent)
    # augment_sent = insert.insert_synonyms_word('万一 您 不想 改善目前 的 情况 的话 ， 我们 会 向 法院 告贵 工厂 ， 也 要 跟 媒体 说 我们 住民 的 困扰 。')
    # print(augment_sent)
    #
    # # 構建SUBSTITUTE類型糾錯 2137+22482
    # augment_sent = substitution.substitute_synonym_word('万一 您 不想 改善目前 的 情况 的话 ， 我们 会 向 法院 告贵 工厂 ， 也 要 跟 媒体 说 我们 住民 的 困扰 。')
    # print(augment_sent)
    # augment_sent = substitution.substitute_homonym_char('万一您不想改善目前的情况的话，我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。', char_pronounce_dict)
    # print(augment_sent)
    # augment_sent = substitution.substitute_shape_char('万一您不想改善目前的情况的话，我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。', char_shape_dict)
    # print(augment_sent)
    #
    # # 構建PARAPHRASE類型糾錯 176+3700
    # augment_sent = local_paraphrase.exchange_word('万一 您 不想 改善目前 的 情况 的话 ， 我们 会 向 法院 告贵 工厂 ， 也 要 跟 媒体 说 我们 住民 的 困扰 。')
    # print(augment_sent)
    # augment_sent = local_paraphrase.exchange_char('万一您不想改善目前的情况的话，我们会向法院告贵工厂，也要跟媒体说我们住民的困扰。')
    # print(augment_sent)

if __name__ == "__main__":
    main()