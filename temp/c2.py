from tamil import utf8

def do_nlp(word):
    return word
    from c3 import do_nlp
    return do_nlp(word)    

def split_tamil_letter(letter):
    """
    Split a Tamil letter into its consonant and vowel components.

    Args:
    letter (str): The Tamil letter to be split.

    Returns:
    tuple: A tuple containing the consonant and vowel components.
    """

    # Tamil consonants (mei) and their corresponding vowel forms (uyirmei)
    consonants = {
        'க்': 'க', 'ச்': 'ச', 'ட்': 'ட', 'த்': 'த', 'ப்': 'ப', 'ற்': 'ற',
        'ஞ்': 'ஞ', 'ண்': 'ண', 'ந்': 'ந', 'ம்': 'ம', 'ன்': 'ன',
        'ய்': 'ய', 'ர்': 'ர', 'ல்': 'ல', 'வ்': 'வ', 'ழ்': 'ழ', 'ள்': 'ள',
        'ஜ்': 'ஜ', 'ஷ்': 'ஷ', 'ஸ்': 'ஸ',
        'ஹ்': 'ஹ', 'க்ஷ்': 'க்ஷ', 'ஸ்ரீ': 'ஸ்ரீ',
    }

    # Tamil short vowels (kuril) and their symbols
    vowels = {
        'அ': '', 'ஆ': 'ா', 'இ': 'ி', 'ஈ': 'ீ', 'உ': 'ு', 'ஊ': 'ூ',
        'எ': 'ெ', 'ஏ': 'ே', 'ஐ': 'ை', 'ஒ': 'ொ', 'ஓ': 'ோ', 'ஔ': 'ௌ',
    }

    # Split the letter into consonant (mei) and vowel (uyir) parts
    for uyir, symbol in vowels.items():
        for mei, consonant in consonants.items():
            if letter == consonant + symbol:
                return (mei, uyir)

    return (letter, '') if letter in consonants else ('', letter)

def remove_last_uyir_letter(word):
    """
    Remove the last uyir letter from a Tamil word.

    Args:
    word (str): The Tamil word to be processed.

    Returns:
    str: The word without the last uyir letter.
    """
    # Get the last letter of the word
    last_letter = utf8.get_letters(word)[-1]
    # Split the letter into consonant (mei) and vowel (uyir) parts
    mei, _ = split_tamil_letter(last_letter)
    # Remove the last uyir letter from the word
    return ''.join(utf8.get_letters(word)[:-1]) + mei

def sandhi_checker(word1, word2):
    """
    Args:
    word1 (str): The first Tamil word.
    word2 (str): The second Tamil word.
    """
    is_miga = None
    # https://www.tnpscjob.com/tnpsc-tamil-santhi-pilaiyai-neekuthal/
    # Rule 2: Question words ending in ஆ, ஓ, ஏ, யா do not combine
    letters = utf8.get_letters(word1)
    last_letter = letters[-1]
    last_uyir_letter = split_tamil_letter(utf8.get_letters(word1)[-1])[1]
    question_words = [
        'அந்த', 'இந்த', 'எந்த', #(adjectives)
        'அது', 'இது', 'எது', #thing
        'அங்கு', 'இங்கு', 'எங்கு', #place
        'அப்பொழுது', 'இப்பொழுது', 'எப்பொழுது', #time
        'அப்படி', 'இப்படி', 'எப்படி', #manner / method
        'அன்று', 'இன்று', 'என்று', #day
        'அவ்வளவு', 'இவ்வளவு', 'எவ்வளவு', #amount
        'அத்தனை', 'இத்தனை', 'எத்தனை', #number
        'அவன்', 'இவன்', 'எவன்', #boy
        'அவள்', 'இவள்', 'எவள்', #girl
        'அவர்', 'இவர்', 'எவர்', #elder
        'அவை', 'இவை', 'எவை', #things
        'யார்', # who?
        'என்ன', # what?
        'ஏன்', # why?
        'எத்தனையாவது', # which rank?
    ]
    if last_uyir_letter in ["ஆ", "ஓ", "ஏ", "யா"] and remove_last_uyir_letter(word1) in question_words:
        is_miga = True

    # Rule 3: வினைத்தொகையில் வல்லினம் மிகாது.
    # Single word

    # Rule 4: Numbers except for எட்டு, பத்து do not combine
    # : Add more numbers
    if (word1 in ["ஒன்று", "இரண்டு", "மூன்று", "நான்கு", "ஐந்து", "ஆறு", "ஏழு", "ஒன்பது",'நூறு','கோடி',]
        or word1.endswith("பது")
    # TODO நூற்றிப்பத்து https://ta.wikisource.org/wiki/பக்கம்:ஆழ்வார்களும்_பாரதியும்.pdf/122#:~:text=என்று தொடங்குகிறது. அத்தொகுதியில்-,நூற்றிப்பத்து,-ஆத்திசூடிப் பாடல்களை பாரதி பாடியுள்ளார். அதில் வையத்தலைமை கொள் என்பதும் ஒன்றாகும். நமது வருங்காலச் செல்வங்களுக்கு பாரதி காட்டு வழி வையத்தலைமை கொள் என்பதாகும்.
    # TODO பதுத் https://ta.wikipedia.org/wiki/கல்பசார்_அணைக்கட்டு#:~:text=ஒரு சிறிய அங்கமான-,பதுத்,-தடுப்பணையின் கட்டுமானம் 2020 முதல் தொடங்க உள்ளது
    ):
        is_miga = True

    # Rule 5: இரட்டைக்கிளவியிலும், அடுக்குத்தொடரிலும் மிகாது.
    if word1 == word2:
        is_miga = True
    
    # 6. வியங்கோள் வினைமுற்றுகளுக்குப் பின் மிகாது.
    # TODO: check condition
    if word1[-1] == 'க':
        is_miga = True
    
    # 7.  https://ta.wikipedia.org/wiki/வடசொல்
    # சங்கீத + சபா = சங்கீதசபா
    if is_வடசொல்(word1) and is_வடசொல்(word2):
        is_miga = True

    # 8. ஈறுகெட்ட எதிர்மறைப் பெயரெச்சம் தவிர மற்ற பெயரெச்சங்களுக்குப் பின் மிகாது.
    if (do_nlp(word1) == 'ADJ' or is_பெயரெச்சம்(word1)) and last_uyir_letter != 'ஆ':
        is_miga = True 
    # கற்ற + சிறுவன் =  கற்ற சிறுவன்
    # சிறிய + பெண் =  சிறிய பெண்
    # stanza check for aa
    # TODO

    # 9. சில ஆறாம் வேற்றுமைத் தொகையில் மிகாது
    # வள்ளுவர் + கருத்து = வள்ளுவர் கருத்து
    if do_nlp(word1) in ['NOUN','PROPN']:
        is_miga = True

    # 10. சில வினையெச்சத் தொடரில் மிகாது.
    if do_nlp(word1) == 'VERB' and detect_குற்றியலுகரம்(word1) in ['மென்றொடர்க் குற்றியலுகரம்','இடைத்தொடர்க் குற்றியலுகரம்']:
        is_miga = True
    # வந்து + பேனான் = வந்துபேனான்
    # செய்து + கொடுத்தாள் = செய்து கொடுத்தாள்
    # TODO

    # 11. சில வினைமுற்றுத் தொடரில் மிகாது.
    # வந்தது + பறவை = வந்தது பறவை
    # சென்றன + குதிரைகள் = சென்றன குதிரைகள்
    # TODO

    # 12.  சில எழுவாய்த் தொடரில் மிகாது
    # சீதை + சென்றாள் =  சீதை சென்றாள்
    # கொக்கு + பறந்தது =  கொக்கு பறந்தது (வன்றொடர்)
    # TODO

    # 13. குற்றியலுகரம், எழுவாய்த்தொடரில் மிகாது, உகர வீற்று வினையெச்சங்கள் முன் மிகாது.
    # வந்து + பார்த்தான் = வந்து பார்த்தான்
    # TODO

    # 14. வல்லின றகர, டகரத்தின் பின் ஒற்று வராது.
    # TODO
    

    # 15. உம்மைத் தொகையில் மிகாது.
    # தாய் + தந்தை = தாய்தந்தை
    # மார்கழி + தை = மார்கழிதை

    
    # 17. படியென்னும் சொல் வினையோடு சேர்ந்து வருமிடத்தில் வல்லினம் மிகாது.
    # வரும்படி + கூறினாள் = வரும்படி கூறினாள்
    # போகும்படி + சொன்னான் = போகும்படி சொன்னான்
    # TODO Detect verb
    if word1.endswith("படி"):
        is_miga = True

    # 18. அது, இது என்னும் சுட்டுகளின் பின்னும் எது, யாது என்னும் வினாச்சொற்களின் பின்னும் மிகாது.
    if word1 in ["அது", "இது", "எது", "யாது",
                "அவை", "இவை",'எவை',
                "அன்று", "இன்று", "என்று",
                "அத்தனை", "இத்தனை", "எத்தனை",
                 ]:
        is_miga = True

    if word1 in [
        'அ', 'இ', 'உ', 'எ',
        'அந்த', 'இந்த', 'அங்கு', 'இங்கு', 'ஆண்டு', 'ஈண்டு', 'அப்படி', 'இப்படி',
        'எந்த', 'எப்படி', 'எங்கு',
        'யாங்கு', 'யாண்டு',
        'அவ்வகை', 'இவ்வகை', 'எவ்வகை',
        'அத்துணை', 'இத்துணை', 'எத்துணை',
    ]:
        is_miga = False
    # 19. சில, பல எனும் சொற்களின் முன் வலி மிகாது.
    if word1 in ["சில", "பல"]:
        is_miga = True

    # 20. விளிப்பெயர் பின் மிகாது
    # TODO
    if word2 in ["போ"]:
        is_miga = True
        
    # 21. இரண்டாம் வேற்றுமைத் தொகையில் மிகாது.
    # தமிழ் + கற்றார் = தமிழ்கற்றார்
    # துணி + கட்டினான் = துணி கட்டினான்
    # TODO

    # 22. அவ்வளவு, இவ்வளவு, எவ்வளவு என்னும் சொற்களின் பின் வலி மிகாது.
    if word1 in ["அவ்வளவு", "இவ்வளவு", "எவ்வளவு",'அவ்வாறு','இவ்வாறு','எவ்வாறு']:
        is_miga = True

    # 23. அஃறிணைப் பன்மை முன் வரும் வல்லினம் மிகாது.

    # பல + பசு = பலபசு
    # சில + கலை = சிலகலை
    # TODO

    # 24. ஏவல்வினை முன் வரும் வல்லினம் மிகாது
    # TODO
    if word1 in ["வா", "எழு"]:
        is_miga = True
    
    # 25. மூன்றாம் வேற்றுமை உருபாகிய ஒடு, ஓடு ஆகியவற்றின் பின்வரும் வல்லினம் மிகாது.
    # கோவலனோடு + கண்ணகி வந்தாள் = கேவலனோடு கண்ணகி வந்தாள்
    # துணிவோடு + செல்க =  துணிவோடு செல்க
    # TODO

    # 26. செய்யிய எனும் வாய்ப்பாட்டு வினையெச்சத்தி பின் வல்லினம் மிகாது
    # காணிய + சென்றேன் = காணிய சென்றேன்
    # உண்ணிய + சென்றான் = உண்ணிய சென்றான்
    # TODO
    if last_letter == 'ய':
        is_miga = True
    
    # 27. பொதுப்பெயர், உயர் திணைப் பெயர்களுக்குப் பின்வரும் வல்லினம் மிகாது
    # தாய் + கண்டாள் = தாய் கண்டாள்
    # கண்ணகி + சீறினள் = கண்ணகி சீறினள்
    # TODO

    # 28. ஐந்தாம் வேற்றுமையின் சொல் ஊருபுகளான இருந்து, நின்று என்பவைகளின் பின் வல்லினம் மிகாது.
    # மரத்திலிருந்து + பறித்தேன் = மரத்திலிருந்து பறித்தேன்
    # மலையின்று + சரிந்தது =மலையினின்று சரிந்தது
    if (
        (word1.endswith("ருந்து") and split_tamil_letter(letters[-4])[1] == 'இ') or
        (word1.endswith("ன்று") and split_tamil_letter(word1[-3])[1] == 'இ')
    ):
        is_miga = True
    # TODO

    # 29. வன்றொடர்க் குற்றியலுகரத்தின் பின் கள், தல் என்னும் விகுதிகள் வரும் போது மிகாது.
    # எழுத்து + கள் = எழுத்துக்கள்
    # போற்று + தல் = போற்றுதல்
    # single word

    if is_miga is None:
        return None, None
    elif not is_miga:
        # Split the first letter of the second word
        mei, uyir = split_tamil_letter(word2[0])
        # Apply the rule: Double the consonant if present
        if uyir:
            word1 =  word1 + mei
        return False, word1
    else:
        return True, []


def is_வினைத்தொகை(word):
    # TODO: stanza bug https://github.com/stanfordnlp/stanza/issues/1319
    lists = [
        'ஊறுகாய்', 'அலைகடல்', 'செய்தவம்',
    ]
    if word in lists:
        return True
    
def is_வடசொல்(word):
    # https://ta.wikipedia.org/wiki/வடசொல்
    lists = 'சங்கீத, சபா, அமலம், அரன், அரி, அவை, உற்பவம், கமலம், காரகம், காரணம், காரியம், காலம், குங்குமம், சத்திரம், சயம், சாகரம், சுகி, ஞானம், நேயம், தசநான்கு, தமாலம், தாரம், திலகம், நட்டம், நிமித்தம், போகி, மூலம், மேரு, யானம், இயோனி, வேணு, கந்தம், சாகரம் – பாகதப் பதிவாகி வந்தவை, நட்டம், கந்தம், சாகரம், நட்டம்'.split(', ')
    if word in lists:
        return True

def is_பெயரெச்சம்(word):
    # TODO: stanza bug https://github.com/stanfordnlp/stanza/issues/1319
    lists = ['கற்ற']
    if word in lists:
        return True

உயிர்_குறில் = 'அ, இ, உ, எ, ஒ'.split(', ')
உயிர்_நெடில் = 'ஆ, ஈ, ஊ, ஏ, ஐ, ஓ, ஒள'.split(', ')
உயிர்_எழுத்துக்கள் = உயிர்_குறில் + உயிர்_நெடில்
is_குறில் = lambda x: x in உயிர்_குறில்
is_நெடில் = lambda x: x in உயிர்_நெடில்
is_உயிர்_எழுத்து = lambda x: x in உயிர்_எழுத்துக்கள்

வல்லின_மெய் = 'க், ச், ட், த், ப், ற்'.split(', ')
மெல்லின_மெய் = 'ங், ஞ், ண், ந், ம், ன்'.split(', ')
இடையின_மெய் = 'ய், ர், ல், வ், ழ், ள்'.split(', ')


def detect_குற்றியலுகரம்(word):
    # TODO: stanza bug
    letters= utf8.get_letters(word)
    last_letter = letters[-1]
    if last_letter not in 'கு, சு, டு, து, பு, று'.split(', '):
        return False
    else:
        if len(letters) == 2 and is_நெடில்(split_tamil_letter(letters[0])[1]):
            return 'நெடிற்றொடர்க் குற்றியலுகரம்'
        elif letters[-2] == 'ஃ':
            return 'ஆய்தத் தொடர்க் குற்றியலுகரம்'
        elif is_உயிர்_எழுத்து(split_tamil_letter(letters[-2])[1]):
            return 'உயிர்த்தொடர்க் குற்றியலுகரம்'
        elif word in ['நுந்தை']:
            return 'மொழிமுதல் குற்றியலுகரம்'
        elif letters[-2] in வல்லின_மெய்:
            return 'வன்றொடர்க் குற்றியலுகரம்'
        elif letters[-2] in மெல்லின_மெய்:
            return 'மென்றொடர்க் குற்றியலுகரம்'
        elif letters[-2] in இடையின_மெய்:
            return 'இடைத்தொடர்க் குற்றியலுகரம்'
            

if __name__ == '__main__':
    words = 'மரத்திலிருந்து சொன்னான்'
    words = words.split(' ')
    words = ["போற்று", "தல்"]
    a = sandhi_checker(*words)
    print(a)

