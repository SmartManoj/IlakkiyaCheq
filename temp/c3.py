import logging
import stanza
from transformers import logging
logging.set_verbosity_error()
stanza.logging.getLogger('stanza').setLevel(logging.ERROR)

# Download and initialize the Tamil model
# stanza.download('ta')
print('Stanza model loading...')
if 1:
    nlp = stanza.Pipeline(lang='ta',package="default_accurate")
else:
    nlp = stanza.Pipeline(lang='ta')
print('Stanza model loaded.')
def do_nlp(text,verbose=False):
    doc = nlp(text)
    # Iterate over the sentences and tokens to print POS tags
    if verbose:
        print(f'{"POS":<7} | {"WORD":<10}')
    res = []
    for sentence in doc.sentences:
        for word in sentence.words:
            if verbose:
                print(f"{word.pos:7} | {word.text}")
            else:
                res.append(word.pos)
    return ' '.join(res)
    print('----------------------')
# Sample text in Tamil
if __name__ == '__main__':
    # for i in ('செய்','தவம்',):
    for i in ('வந்து, செய்து',):
        print(i,do_nlp(i))
