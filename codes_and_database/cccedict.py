"""CC-CEDICT."""

import gzip
import re
from pathlib import Path
from typing import Dict, List, Optional, TextIO, Union

PinyinToneMark = {
    0: "aoeiuv\u00fc",
    1: "\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: "\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: "\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: "\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}

PinyinToneMark2 = {
    'a': "aāáǎà",
    'e': "eēéěè",
    'i': "iīíǐì",
    'o': "oōóǒò",
    'u': "uūúǔù",
    'v': "üǖǘǚǜ",
}

class CcCedict:
    """CC-CEDICT."""

    def __init__(self) -> None:
        path = Path(__file__).parent / 'data' / 'cedict_1_0_ts_utf-8_mdbg.txt.gz'
        with gzip.open(path, mode='rt', encoding='utf-8') as file:
            self._parse_file(file)

    def get_definitions(self, chinese: str) -> Optional[List]:
        """Gets definitions."""
        return self._get_field(field='definitions', chinese=chinese)

    def get_pinyin(self, chinese: str) -> Optional[str]:
        """Gets pinyin."""
        return self._get_field(field='pinyin', chinese=chinese)

    def get_simplified(self, chinese: str) -> Optional[str]:
        """Gets simplified."""
        return self._get_field(field='simplified', chinese=chinese)

    def get_traditional(self, chinese: str) -> Optional[str]:
        """Gets traditional."""
        return self._get_field(field='traditional', chinese=chinese)

    def get_entry(self, chinese: str) -> Optional[Dict]:
        """Gets an entry."""
        # Check traditional.
        if chinese in self.traditional_to_index:
            i = self.traditional_to_index[chinese]
            return self.entries[i]
        
        # Check simplified.
        if chinese in self.simplified_to_index:
            i = self.simplified_to_index[chinese]
            return self.entries[i]

        return None
    
    # Using both Chinese and pinyin to get the meaning. 
    def get_entry_2(self, chinese: str, pinyin: str) -> Optional[Dict]:
        """Gets an entry."""
        # Check traditional.
        if chinese in self.traditional_to_index:
            for entry in self.entries:
                if entry['traditional'] == chinese and entry['pinyin'] == pinyin and entry['proper'] == False:
                    return entry
            for entry in self.entries:
                if entry['traditional'] == chinese and entry['pinyin'] == pinyin and entry['proper'] == True:
                    return entry
            
        return None
    
    def decode_pinyin(self, s):
        s = s.lower()
        r = ""
        t = ""
        for c in s:
            if (c >= 'a' and c <= 'z'):
                t += c
            elif c == ':':
                assert t[-1] == 'u'
                t = t[:-1] + "\u00fc"
            else:
                if c >= '0' and c <= '5':
                    tone = int(c) % 5
                    if tone != 0:
                        m = re.search("[aoeiuv\u00fc]+", t)
                        if m is None:
                            t += c
                        elif len(m.group(0)) == 1:
                            t = t[:m.start(0)] + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))] + t[m.end(0):]
                        else:
                            if 'a' in t:
                                t = t.replace("a", PinyinToneMark[tone][0])
                            elif 'o' in t:
                                t = t.replace("o", PinyinToneMark[tone][1])
                            elif 'e' in t:
                                t = t.replace("e", PinyinToneMark[tone][2])
                            elif t.endswith("ui"):
                                t = t.replace("i", PinyinToneMark[tone][3])
                            elif t.endswith("iu"):
                                t = t.replace("u", PinyinToneMark[tone][4])
                            else:
                                t += "!"
                r += t
                t = ""
        r += t
        return r
            
    def get_entries(self) -> List:
        """Gets all entries."""
        return self.entries

    def _get_field(self, field: str, chinese: str) -> Union[str, List, None]:
        """Gets field."""
        entry = self.get_entry(chinese)
        if entry is None:
            return None

        return entry[field]

    def _parse_file(self, file: TextIO) -> None:
        self.entries = []
        self.simplified_to_index = {}
        self.traditional_to_index = {}
        i = 0

        for line in file:
            entry = self._parse_line(line)
            if entry is None:
                continue

            # Add entry.
            self.entries.append(entry)

            # Share entries for simplified and traditional.
            simplified = entry['simplified']
            traditional = entry['traditional']
            self.simplified_to_index[simplified] = i
            self.traditional_to_index[traditional] = i
            i += 1

    def _parse_line(self, line: str) -> Optional[Dict]:
        # Skip comments.
        if line.startswith('#'):
            return None

        # Strip whitespace and trailing slash.
        line = line.strip()
        line = line.rstrip('/')

        # Get chinese parts.
        chinese, english = line.split('/', maxsplit=1)
        chinese = chinese.strip()
        traditional_and_simplified, pinyin = chinese.split('[')
        traditional_and_simplified = traditional_and_simplified.strip()
        traditional, simplified = traditional_and_simplified.split()

        # Remove brackets around pinyin.
        proper = False # proper noun
        pinyin = pinyin[:-1]
        if pinyin[0].isupper():
            proper = True
        pinyin = self.decode_pinyin(pinyin)

        # Get english definitions.
        senses = english.split('/')
        glosses = [re.split(';|,', sense) for sense in senses]
        definitions = [definition for gloss in glosses for definition in gloss]
        definitions = [definition.strip() for definition in definitions]

        return {
            'traditional': traditional,
            'simplified': simplified,
            'pinyin': pinyin,
            'definitions': definitions,
            'proper': proper,
        }
