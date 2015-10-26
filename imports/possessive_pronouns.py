# coding: utf-8
import re

__author__ = 'shtrih'

# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class possessive_pronouns:
    replaces = {
        # ед. ч. муж. р.
        'мой':   'твой',
        'твой': 'мой',
        'моём': 'твоём',
        'твоём': 'моём',
        'моем': 'твоем',
        'твоем': 'моем',
        'ваш': 'наш',
        'наш': 'ваш',

        # ед. ч. жен. р.
        'моя':  'твоя',
        'твоя': 'моя',
        'моей': 'твоей',
        'твоей': 'моей',
        'ваша':  'наша',
        'наша':  'ваша',

        # ед. ч. ср. р.
        'моё': 'твоё',
        'твоё': 'моё',
        'мое':  'твое',
        'твое': 'мое',
        'ваше': 'наше',
        'наше': 'ваше',

        # мн. ч.
        'вашим': 'нашим',
        'нашим': 'вашим',
        'мои':  'твои',
        'твои': 'мои',
        'ваши': 'наши',
        'наши': 'ваши',
        'нам': 'вам',
        'вам': 'нам',
        'мы':    'вы',
        'вы':    'мы',

        'я':     'ты',
        'ты':    'я',
        'мне':   'тебе',
        'тебе':  'мне',
        'меня':  'тебя',
        'тебя':  'меня',
        'тобой': 'мной',
        'мной':  'тобой',
    }

    def invert(self, text=u''):
        """ Заменяет местоимения на противоположные. Например, взял мой стакан → взял твой стакан """
        result = text
        replaced = []

        for k, v in self.replaces.iteritems():
            if v not in replaced:
                regex = re.compile(ur'\b({0})\b'.format(re.escape(k.decode('utf-8'))), re.I | re.U)
                # res = regex.search(result)
                # if res is not None:
                #     logging.debug(res.groups())

                resultn = re.subn(regex, v.decode('utf-8'), result, 0)
                result = resultn[0]
                if resultn[1] > 0:
                    replaced.append(k)

        # logging.debug(text + u" → " + result)
        return result

_inst = possessive_pronouns()
invert = _inst.invert

# print(invert(u'Кто лизал мои тапки?'))
# print(invert(u'Моё место заняли?'))
# print(invert(u'Это ваши ласты?'))