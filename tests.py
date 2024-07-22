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
m = [{'eg_or_rus': 'ruslan', 'scaner_name': 'odds_portal', 'bettors_name': 'guillemm5', 'timeStart': '10:00 03.08.2024', 'players': 'Valentine–Adamstown Rosebud', 'bet': 'Обе забьют Нет', 'coefficient': 2.46, 'sport': 'Футбол', 'sp_tg': 'Football', 'coef_tg': '1.910 - 2.50100 (PICK)', 'lnk': 'https://www.oddsportal2.com/football/australia/npl-northern-nsw/valentine-adamstown-rosebud-ltg40Oh5/#bts;2', 'country': 'Australia (Npl Northern Nsw)', 'bet_tg': 'BTS'}]
from pprint import pprint

for item in m:
    del item['bet_tg']
    del item['sp_tg']
    del item['lnk']
    del item['country']
    del item['coef_tg']

pprint(m)
