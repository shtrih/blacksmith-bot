# coding: utf-8
import re

__author__ = 'shtrih'

# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class possessive_pronouns:
    replaces = {
        u'мой':  u'твой',
        u'твой': u'мой',
        u'мои':  u'твои',
        u'твои': u'мои',
        u'моё':  u'твоё',
        u'твоё': u'моё',
        u'мое':  u'твое',
        u'твое': u'мое',
        u'ваш':  u'наш',
        u'наш':  u'ваш',
        u'ваши': u'наши',
        u'наши': u'ваши',
        u'ваше': u'наше',
        u'наше': u'ваше',
        u'я':    u'ты',
        u'ты':   u'я',
        u'мы':   u'вы',
        u'вы':   u'мы',
    }

    """ Заменяет местоимения на противоположные. Например, взял мой стакан → взял твой стакан """
    def invert(self, text=u''):
        result = text
        replaced = []

        for k, v in self.replaces.iteritems():
            if v not in replaced:
                regex = re.compile(ur'\b({0})\b'.format(re.escape(k)), re.I | re.U)
                # res = regex.search(result)
                # if res is not None:
                #     logging.debug(res.groups())

                resultn = re.subn(regex, v, result, 0)
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