import re

from googletrans import Translator


def text_translator(text, src='en', dest='ru'):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        if re.search(r"[a-zA-Z]", translation.text):
            translation = translator.translate(text=text, src=src, dest=dest)

        return translation.text
    except Exception as ex:
        print('Translator err: ', ex)
        return text


# print(text_translator('Gold Coast Utd - Olympic FC'))
d = '/tennis/germany/atp-hamburg/baez-sebastian-arthur-fils-QkK3uLUI/#home-away;2'
m = list(map(lambda i: i.title().replace('-', ' '), d.split('/')[2:4]))[::-1]