# Version 1.1

class LanguageNotProvided(Exception):
    def __init__(self, lang: str):
        super().__init__(f"This phrase does not support this language ({lang})")


class LanguageCodeShouldBeString(Exception):
    def __init__(self, value):
        super().__init__(f"Language code should be <str> type (<{type(value)}> provided instead)")


class PhraseShouldBeString(Exception):
    def __init__(self, value):
        super().__init__(f"Phrase should be <str> type (<{type(value)}> provided instead)")


class __BasePhrase(object):
    _storage: dict

    def __init__(self):
        self._storage = dict()

    def __get_value(self, lang: str):
        if not isinstance(lang, str):
            raise LanguageCodeShouldBeString(lang)

        if lang not in self._storage.keys():
            raise LanguageNotProvided(lang)

        return self._storage[lang.lower()]

    def __set_value(self, lang, phrase):
        if not isinstance(lang, str):
            raise LanguageCodeShouldBeString(lang)

        if not isinstance(phrase, str):
            raise PhraseShouldBeString(phrase)

        setattr(self, lang.lower(), phrase)
        self._storage[lang.lower()] = phrase

    def __getitem__(self, item):
        return self.__get_value(item)

    def __setitem__(self, key, value):
        return self.__set_value(key, value)

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, item):
        raise LanguageNotProvided(item)


class Phrase(__BasePhrase):
    _storage: dict

    def __init__(self, **kwargs):
        super().__init__()
        for item in kwargs.items():
            lang, phrase = item[0], item[1]
            if isinstance(lang, str) and isinstance(phrase, str):
                self.__setitem__(lang, phrase)

    def __repr__(self):
        return f"<Phrase: {self._storage}>"
