# In Brief

This GitHub repository contains the TOCFL vocabulary list *with English translation* and its building Python files according to the comprehensive official vocabulary list for the TOCFL test by Taiwan's National Academy for Educational Research (國家教育研究院 or 國教院 for short). The file comprises 14425 words from all difficulties and their meaning. Primarily, the definition in this vocabulary list refers to the CC-CEDICT, on which MDBG and Pleco rely.

You can download the file (TOCFL_14425_word_list.xlsx) directly.

# In details

TOCFL is the Chinese test for foreigners who focus on Taiwanese Mandarin. Currently, there are two main official vocabulary lists on the website, which are:

1. The 8000 words listed by the Steering Committee for the Test Of Proficiency-Huayu (SC-TOP) or 國家華語測驗推動工作委員會.
2. The 14425 words listed by the National Academy for Educational Research or 國家教育研究院 (or 國教院 for short).

The 8000 words listed by the SC-TOP already have their English translation, and I have also provided them in this repository. However, I found personally that those 8000 words are not really comprehensive when compared to the 14425 words listed by the 國教院. However, the word list from the 國教院 does not have an English translation yet, so I have translated those words accordingly.

The translation is done mainly using Python code and the CC-CEDICT database. However, there are some important difficulties that I want to list here:

1. Around 380 words are not in the CC-CEDICT database, so I need to do the translation manually by looking at other dictionary websites (mostly from the dictionary of Taiwan's Ministry of Education, but some are also from Zdic, Baidu, etc.) You can see the word list that I have to do manual translation in out_loss_trans.csv. I have tried my best to do those translations.
2. Some words have different readings between Mainland and Taiwanese versions. Some Mainland Mandarin words have one-to-one reading correspondence with Taiwanese Mandarin words. Some have two-to-one reading correspondence. I have tried my best to translate those words accordingly, and I'm not a linguistic person, so please expect some errors.
3. You can see how the translation is done in detail in the dev.py file. I will do the documentation later if there are interesting people who come and ask how I got this translation.

Please feel free to use it. Hope you enjoy language learning. If there are errors, feel free to contact me as well.

# Hats off to

1. Patrick Pei and his repo https://github.com/patrickpei/pycccedict. I use your code a lot.
2. The one who creates the CC-CEDICT.
3. 國家教育研究院

# Why am I doing this

Beginner's word lists are plenty, but when you are stuck at the intermediate level, you finally realize that you need a more comprehensive word list to accommodate your continuation of the learning journey. You finally found out that you heard the word 飆車 and wondered why you hadn't known about the character 飆 before.

Of course, you can learn Chinese gradually by just remembering the words when you first encounter them. Still, it would be better (from my personal point of view) to learn in two ways: learn the word from the vocab list, so you still have some hints, and learn it from real life so you know how to actually use that word.

So this is why I translated those 14425 words and shared them here.

