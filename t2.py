from pprint import pprint
from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()
parser.set_default_language('tamil')



def get_word(word):
    word = parser.fetch(word,)
    pprint(word)


# features
parser.exclude_part_of_speech('noun')
parser.include_relation('alternative forms')

if __name__ == '__main__':
    get_word('பகல்')