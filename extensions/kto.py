# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  kto.py

# from BlackSmith import GROUPCHATS

__author__ = 'shtrih'

from random import randint
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handler_kto(type, source, body):
    list = [
        "Вне всякого сомнения %(action)s конечно же %(nick)s. Инфа 100%%.",
        "%(action)s стопроцентно %(nick)s. Мне мой знакомый сказал, которому я доверяю.",
        "Кто %(action)s, говоришь? Я не буду пальцем показывать, да и %(nick)s расстроится."
    ]
    users = [
        'ты'
    ]

    if source[1] in GROUPCHATS:
        users = GROUPCHATS[source[1]].keys()
        # logging.debug(users)

    reply(type, source, list[ randint(0, len(list)-1) ] % {"action": body[:-1], "nick" : users[ randint(0, len(users)-1) ]})

command_handler(handler_kto, 10, "kto")