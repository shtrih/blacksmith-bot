# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  kto.py

# from BlackSmith import GROUPCHATS

__author__ = 'shtrih'

from random import randint
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: обработка случаев с «мои=твои», мой=твой», я=ты
# Кто обмазался моим несвежим говном и отчаянно мастурбирует?
# Кто я?
# Кто лизал мои тапки?
# http://puu.sh/kSftk/1b25ea57f4.png

def handler_kto(type, source, body):
    list = [
        "Вне всякого сомнения %(action)s конечно же %(nick)s. Инфа 100%%.",
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
        'ты'
    ]

    if source[1] in GROUPCHATS:
        users = GROUPCHATS[source[1]].keys()
        # logging.debug(users)

    reply(type, source, list[ randint(0, len(list)-1) ] % {"action": body[:-1], "nick" : users[ randint(0, len(users)-1) ]})

command_handler(handler_kto, 10, "kto")