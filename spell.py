
from tamilspellchecker.TamilSpellingAutoCorrect import TamilSpellingAutoCorrect, get_data
from pprint import pprint
from tamil.utf8 import get_letters
spellchecker = TamilSpellingAutoCorrect(get_data("tamil_bloom_filter.txt"), get_data("tamilwordlist.txt"))

def prioritize_suggestions(word, suggestions):
    # Define the common mistake pattern
    mistake_patterns = [("ன", "ண"), ("ண", "ன")]

    # Prioritize words that correct the mistake
    priority_list = []
    regular_list = []

    for suggestion in suggestions:
        if any(word.replace(mistake[0], mistake[1]) == suggestion or word.replace(mistake[1], mistake[0]) == suggestion for mistake in mistake_patterns):
            priority_list.append(suggestion)
        else:
            regular_list.append(suggestion)

    # Combine the two lists: priority first, then regular
    prioritized_suggestions = priority_list + regular_list

    return prioritized_suggestions
def correct_spelling(s):
    output = []
    for word in s.split():
        wl=(len(get_letters(word)))
        results = spellchecker.tamil_Norvig_correct_spelling(word) #தமிழ்நாடு என்பது சரியான சொல்.
        # results = list(filter(lambda x: len(get_letters(x)) == wl,results )) #and for words <= 6 letters
        # Using the function
        prioritized_results = prioritize_suggestions(word, results)
        if prioritized_results:
            # print(prioritized_results[0])
            output.append(prioritized_results[0])
            pass
        else:
            # print(word, 'correct')
            output.append(word)
            pass

    # print('corrected spelling: ', ' '.join(output))
    return ' '.join(output)

if __name__ == '__main__':
    s = "வனக்கம் நாண் நாலை நண்பகல் நண்பர்களுடன் நன்பன் திரைப்படம் பார்க்க போகிறேன்"
    correct_spelling(s)
# print(results.index('வணக்கம்'))
# pprint(results)
# assert 'தமிழ்நாடு' in results

    