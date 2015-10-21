# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin

# from BlackSmith import GROUPCHATS

__author__ = 'shtrih'

import re
from random import randint
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handler_vanguy(type, source, body):
    list_or = [
        "%s, да. Инфа 100%%.",
        "%s.",
        "%s. Мне мой знакомый сказал, которому я доверяю.",
        "Точно %s, мне Спок-кот из альтернативной Вселенной сказал, что так будет.",
        "Тебе уебать? %s, ясен пень",
        "Чтобы %s? Да никогда в жизни",
    ]
    list_bin = [
        "%s — никогда!",
        "%s? Забудь об этом",
        "%s? Да, хотя зря.",
        "%s, инфа сотка",
    ]

    match = re.match(u"\s*[,:]?\s*(.*[^\s])\s+или\s+(.*[^\s.?])[.?]?", body, re.U | re.I)
    if match is not None:
        # logging.debug(match.groups())
        selected = match.group(randint(1, 2))
        selected = selected[0].upper() + selected[1:]

        message = list_or[randint(0, len(list_or) - 1)] % selected

    match = re.match(u"\s*[,:]?\s*(.*[^\s.?])[.?]?", body, re.U | re.I)
    if match is not None:
        selected = match.group(1)
        selected = selected[0].upper() + selected[1:]

        message = list_bin[randint(0, len(list_bin) - 1)] % selected

    reply(type, source, message)

command_handler(handler_vanguy, 10, "vanguy")