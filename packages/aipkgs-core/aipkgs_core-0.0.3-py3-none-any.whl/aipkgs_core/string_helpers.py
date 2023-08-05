from emoji import UNICODE_EMOJI


def is_emoji(s):
    for lang in UNICODE_EMOJI:
        if s in UNICODE_EMOJI[lang]: return True
    return False


def contains_emoji(txt: str):
    for c in txt:
        if is_emoji(c):
            return True
    return False


def contains_special_characters(txt: str):
    special_characters = "!@#$%^&*"
    count = 0
    for sc in special_characters:
        count += txt.count(sc)
        if count > 1:
            return True
    return bool(count)


def contains_mal_phrases(txt: str):
    phrases = ['sex', 'porn']
    count = 0
    for sc in phrases:
        count += txt.count(sc)
        if count > 1:
            return True
    return bool(count)


def is_validate(txt: str):
    if contains_emoji(txt=txt) or contains_special_characters(txt=txt) or contains_mal_phrases(txt=txt):
        return False
    return True
