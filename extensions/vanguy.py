# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
from imports.possessive_pronouns import invert

execfile("imports/command_handler_custom.py")

__author__ = 'shtrih'

import re
from random import randint, choice
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        "Нет, инфа %d%%",
        "Что? %s? Ты что, ёбнулся, конечно нет!",
        "Ни в коем случае не %s.",

        "%s — Да, хотя зря.",
        "%s, инфа сотыга",
        "Да, инфа %d%%",
        "%s. Я гарантирую.",
        "%s. Без вариантов.",
    ]

    match = re.match(ur"\s*(.*[^\s])\s+или\s+(.*[^\s.?])[.?]?", body, re.U | re.I)
    if match is not None:
        # logging.debug(match.groups())
        selected = invert(match.group(randint(1, 2)))
        # selected = selected[0].upper() + selected[1:]

        message = choice(list_or) % selected
        reply(type, source, message)
    else:
        match = re.match(ur"\s*(.*[^\s.?])[.?]?", body, re.U | re.I)
        if match is not None:
            selected = invert(match.group(1))
            # selected = selected[0].upper() + selected[1:]
            message = choice(list_bin)
            if message.find('%d') != -1:
                message %= randint(0, 101)
            else:
                message %= selected

            reply(type, source, message)

# command_handler(handler_vanguy, 10, "vanguy")
command_handler_custom(handler_vanguy, 10, "vanguy")