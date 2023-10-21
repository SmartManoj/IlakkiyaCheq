def generate_homophones(word):
    # List of characters that can be replaced to generate potential homophones
    substitutions = [
        ["ன","ண"],
        ["ள","ல","ழ"],
        ['ர','ற'],
    ]

    # Recursive function to generate homophones
    def _generate_homophones(w, index=0):
        if index == len(w):
            return [w]

        char = w[index]

        # Check if the current character is in any of the substitution groups
        possibilities = [char]  # At least the character itself
        for group in substitutions:
            if char in group:
                possibilities.extend([g for g in group if g != char])
                break

        homophones = []
        for possibility in possibilities:
            for homophone in _generate_homophones(w[:index] + possibility + w[index+1:], index+1):
                homophones.append(homophone)

        return homophones

    return _generate_homophones(word)

word = "நண்பகல்"
homophones = generate_homophones(word)
print(homophones)

from tamilspellchecker.TamilwordChecker import TamilwordChecker
from tamilspellchecker.TamilSpellingAutoCorrect import get_data

unique_word_count = 2043478
tamilwordchecker = TamilwordChecker(unique_word_count,get_data("tamil_bloom_filter.txt"))
    
homophones = [i for i in homophones if tamilwordchecker.tamil_word_exists(i)]
#     from t2 import get_word
#     get_word(i)
print(homophones)