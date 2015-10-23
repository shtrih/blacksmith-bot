# coding: utf-8
import re

__author__ = 'shtrih'

# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class possessive_pronouns:
    replaces = {
        'мой':   'твой',
        'твой':  'мой',
        'моём':  'твоём',
        'твоём': 'моём',
        'моем':  'твоем',
        'твоем': 'моем',
        'вашим': 'нашим',
        'нашим': 'вашим',
        'мои':   'твои',
        'твои':  'мои',
        'моё':   'твоё',
        'твоё':  'моё',
        'мое':   'твое',
        'твое':  'мое',
        'ваш':   'наш',
        'наш':   'ваш',
        'ваши':  'наши',
        'наши':  'ваши',
        'ваша':  'наша',
        'наша':  'ваша',
        'ваше':  'наше',
        'наше':  'ваше',
        'я':     'ты',
        'ты':    'я',
        'мы':    'вы',
        'вы':    'мы',
        'мне':   'тебе',
        'тебе':  'мне',
        'нам':   'вам',
        'вам':   'нам',
        'меня':  'тебя',
        'тебя':  'меня',
        'тобой': 'мной',
        'мной':  'тобой',
    }

    """ Заменяет местоимения на противоположные. Например, взял мой стакан → взял твой стакан """
    def invert(self, text=u''):
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