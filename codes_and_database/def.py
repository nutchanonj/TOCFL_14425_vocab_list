# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 00:44:59 2024

@author: nutch
"""

#%% ------------------------------------------------------

from cccedict import CcCedict
import pandas as pd
import re

cccedict = CcCedict()
df = pd.read_csv('Vocabulary_List.csv')

#%%

PinyinToneMark2 = {
    'a': "aāáǎà",
    'e': "eēéěè",
    'i': "iīíǐì",
    'o': "oōóǒò",
    'u': "uūúǔù",
    'v': "üǖǘǚǜ",
}

def alternate_read(s):
    r = ""
    for i in range(len(s)-1, 0, -1):
        if s[i] in PinyinToneMark2["a"]:
            r = s[:i] + PinyinToneMark2["a"][0] + s[i + 1:]
            break
        elif s[i] in PinyinToneMark2["e"]:
            r = s[:i] + PinyinToneMark2["e"][0] + s[i + 1:]
            break
        elif s[i] in PinyinToneMark2["i"]:
            r = s[:i] + PinyinToneMark2["i"][0] + s[i + 1:]
            break
        elif s[i] in PinyinToneMark2["o"]:
            r = s[:i] + PinyinToneMark2["o"][0] + s[i + 1:]
            break
        elif s[i] in PinyinToneMark2["u"]:
            r = s[:i] + PinyinToneMark2["u"][0] + s[i + 1:]
            break
        elif s[i] in PinyinToneMark2["v"]:
            r = s[:i] + PinyinToneMark2["v"][0] + s[i + 1:]
            break
    return r

#%% ------------------------------------------------------

# Words with the same writing warning.
def warning(row):
    print(row['序號'])
    return bool(re.search(r'\d', row['詞語']))

df['warning'] = df.apply(warning, axis=1)

# Remove the number in that file.
def remove_num(row):
    print(row['序號'])
    return re.sub('[1-9]', '', row['詞語'])

df['詞語'] = df.apply(remove_num, axis=1)

# Find definitions
def label_def(row):
    print(row['序號'])
    traditional = row['詞語'].split('/')[0]
    pinyin = row['參考漢語拼音'].split('/')[0]
    entry = cccedict.get_entry_2(traditional, pinyin)
    if entry != None:
        return ", ".join(entry['definitions'])
    elif entry == None and row['warning'] == False:
        entry = cccedict.get_entry(traditional)
        if entry != None:
            return ", ".join(entry['definitions'])
        elif '/' in row['詞語']:
            traditional = row['詞語'].split('/')[1]
            entry = cccedict.get_entry(traditional)
            if entry != None:
                return ", ".join(entry['definitions'])
            else:
                print("์Not found!")
                print(row['序號'])
                print(row['級別'])
        else:
            print("Not found!")
            print(row['序號'])
            print(row['級別'])
    else:
        print("Not found!")
        print(row['序號'])
        print(row['級別'])

df['definition'] = df.apply(label_def, axis=1)
df.to_csv("out.csv", encoding='utf-8')
df_loss = df.loc[df['definition'].isnull()]
df_loss.to_csv("out_loss.csv", encoding='utf-8')

#%%

fields = ['序號', '詞語', '等別', '級別', '情境', '書面字頻(每百萬字)', '口語字頻(每百萬字)', '簡編本系統號',
       '參考注音', '參考漢語拼音', 'warning', 'definition']
df = pd.read_csv('out.csv', usecols=fields)
df = df.astype({"definition": str})

# Replace the "variant of ..." cells.
def variant(row):
    if row['definition'].find("variant of ") == 0:
        print(row['序號'])
        chinese_find = re.findall('variant of (.*)\[', row['definition'])
        print(chinese_find)
        if len(chinese_find) == 0:
            chinese_find = re.findall('variant of (.*)\|', row['definition'])
            print(chinese_find)
        chinese_find = chinese_find[0].split('|')[0]
        entry = cccedict.get_entry(chinese_find)
        if entry != None:
            return ", ".join(entry['definitions'])
    return row['definition']

df['definition'] = df.apply(variant, axis=1)
df.to_csv("out.csv", encoding='utf-8')

#%%

fields = ['序號', '詞語', '等別', '級別', '情境', '書面字頻(每百萬字)', '口語字頻(每百萬字)', '簡編本系統號',
       '參考注音', '參考漢語拼音', 'warning', 'definition']
df_loss_trans = pd.read_csv('out_loss_trans.csv', usecols=fields)
df = pd.read_csv('out.csv', usecols=fields)

# Add my own definitions, which are not exist in CC-CEDICT.
for index, row in df_loss_trans.iterrows():
    num = row['序號']
    print(num)
    df.at[num-1, 'definition'] = row['definition']

df.to_csv("out.csv", encoding='utf-8')

#%%

fields = ['序號', '詞語', '等別', '級別', '情境', '書面字頻(每百萬字)', '口語字頻(每百萬字)', '簡編本系統號',
       '參考注音', '參考漢語拼音', 'warning', 'definition']
df = pd.read_csv('out.csv', usecols=fields)

# Alternate reading in Mainland China, which CC-CEDICT relies on.
def alt_read_warning(row):
    traditional = row['詞語'].split('/')[0]
    pinyin = row['參考漢語拼音'].split('/')[0]
    alt_pinyin = alternate_read(pinyin)
    if alt_pinyin != pinyin:
        entry = cccedict.get_entry_2(traditional, pinyin)
        entry_alt = cccedict.get_entry_2(traditional, alt_pinyin)
        if entry != None and entry_alt != None:
            print(row['序號'])
            return ", ".join(entry['definitions'] + entry_alt['definitions'])
        else:
            return row['definition']
    else:
        return row['definition']

df['definition'] = df.apply(alt_read_warning, axis=1)

fields_fin = ['序號', '詞語', '等別', '級別', '情境', '書面字頻(每百萬字)', '口語字頻(每百萬字)', '簡編本系統號',
       '參考注音', '參考漢語拼音', 'definition']
    
df.to_csv("out.csv", encoding='utf-8', columns=fields_fin)


