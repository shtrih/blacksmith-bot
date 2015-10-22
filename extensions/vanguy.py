# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin

execfile("imports/command_handler_custom.py")

__author__ = 'shtrih'

import re
from random import randint, choice
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handler_vanguy(type, source, body):
    list_or = [
        "%s, да. Инфа 100%%.",
        "%s.",
        "%s. Мне мой знакомый сказал, которому я доверяю.",
        "Точно %s, мне Спок-кот из альтернативной Вселенной сказал.",
        "Тебе уебать? %s, ясен пень",
        "%s? Да никогда в жизни",
        "Очевидно, что %s, другого не дано.",
        "Упорот чтоль, явно же %s.",
        "Когда ты уже начнёшь сам решать? %s.",
    ]
    list_bin = [
        "%s — никогда!",
        "%s? Забудь об этом",
        "%s — Да, хотя зря.",
        "%s, инфа сотыга",
        "Да, инфа %d%%",
    ]

    match = re.match(u"\s*(.*[^\s])\s+или\s+(.*[^\s.?])[.?]?", body, re.U | re.I)
    if match is not None:
        # logging.debug(match.groups())
        selected = match.group(randint(1, 2))
        # selected = selected[0].upper() + selected[1:]

        message = choice(list_or) % selected
        reply(type, source, message)
    else:
        match = re.match(u"\s*(.*[^\s.?])[.?]?", body, re.U | re.I)
        if match is not None:
            selected = match.group(1)
            # selected = selected[0].upper() + selected[1:]
            message = choice(list_bin)
            if message == list_bin[4]:
                message %= randint(0, 101)
            else:
                message %= selected

            reply(type, source, message)

# command_handler(handler_vanguy, 10, "vanguy")
command_handler_custom(handler_vanguy, 10, "vanguy")