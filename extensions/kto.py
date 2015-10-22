# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  kto.py

# from BlackSmith import GROUPCHATS
from imports.possessive_pronouns import invert

__author__ = 'shtrih'

from random import choice

# http://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handler_kto(type, source, body):
    list = [
        "Вне всякого сомнения, %(action)s конечно же %(nick)s. Инфа 100%%.",
        "%(action)s стопроцентно %(nick)s. Мне мой знакомый сказал, которому я доверяю.",
        "Кто %(action)s, говоришь? Я не буду пальцем показывать, да и %(nick)s расстроится.",
        "Я уверена, что %(action)s спидовый %(nick)s!",
        "Ты можешь мне не верить, но %(action)s именно %(nick)s.",
        "Из надёжных источников, которые я палить не собираюсь, мне стало известно, что %(action)s %(nick)s.",
        "%(action)s без вариантов %(nick)s! Мне бабушка рассказывала, она у меня ясновидящая!",
        "Скорее всего, %(action)s наш %(nick)s, это так похоже на него.",
        "Кто %(action)s… Думаю это %(nick)s, смотри как занервничал, когда ты спросил.",
        "Очевидно, что %(action)s %(nick)s, другого не дано.",
    ]
    users = [
        'ты сам'
    ]

    if source[1] in GROUPCHATS:
        users = GROUPCHATS[source[1]].keys()
        # logging.debug(users)

    # если последний символ не буквоцифра, значит знак препинания. Отрезаем.
    if not body[-1::1].isalnum():
        body = body[:-1]

    # logging.debug(invert(body))

    message = choice(list) % {"action": invert(body), "nick": choice(users)}

    reply(type, source, message)

command_handler(handler_kto, 10, "kto")