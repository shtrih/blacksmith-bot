# BS mark.1-55
# coding=utf-8
import re
import operator

__author__ = 'shtrih'

"""
добавь жид shtrh жид@жид
добавь алиас shtrih штрих
профиль [shtrih]

лойс/зашквор ник[:,]
топ 10
дно 10
"""
execfile("imports/command_handler_custom.py")

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# {'foo@conference.j.ru': {'main_jid': {entities, …}}}
gProfiles = {}

# {'foo@conference.j.ru': {'main_nickname': 'main_jid', …}}
gUsers = {}

# {'foo@conference.j.ru': {main_nickname: ['alias1', 'alias2', …]}}
gAliases = {}

# {'foo@conference.j.ru': {main_jid: ['jid1', 'jid2', …]}}
gJids = {}
gLoaded = False

LOISES =    'loises'
ZASHKVARS = 'zashkvars'
BUTTHURTS = 'butthurts'
TOLSTO =    'tolsto'
DVACHAYA =  'dva_chaya'
SAGE =      'sage'

gEntities = {
    LOISES:    'Лойсы',
    ZASHKVARS: 'Зашквары',
    BUTTHURTS: 'Багеты',
    TOLSTO:    'Толсто',
    DVACHAYA:  'Два чая',
    SAGE:      'Сажи',
}

def handler_add_router(type, source, body):
    arguments = filter(bool, map(unicode.strip, body.split(' ')))
    command = arguments.pop(0)
    if re.match(ur'(юзер[а-я]?|профиль)', command, re.I | re.U):
        for arg in arguments:
            _add_user(type, source, arg)

    elif re.match(ur'(алиас|имя|ник(|нейм))', command, re.I | re.U):
        _add_alias(type, source, arguments)

    elif re.match(ur'(д?жид|jid)', command, re.I | re.U):
        _add_jid(type, source, arguments)

def _add_alias(type, source, arguments):
    global gAliases

    if len(arguments) >= 2:
        conference = source[1]
        nickname_to = arguments[0]
        alias = arguments[1]

        main_nickname = _get_main_nickname(nickname_to, conference)
        if gAliases.has_key(conference) and main_nickname is not None:
            if alias not in gAliases[conference][main_nickname]:
                gAliases[conference][main_nickname].append(alias)
                _save_profiles(conference)
            message = 'Ok'
        else:
            message = 'Не зарегистрирован'
    else:
        message = 'Нехватает аргументов.'

    reply(type, source, message)

def _add_jid(type, source, arguments):
    pass

def _add_user(type, source, body):
    global gProfiles, gEntities, gUsers

    message = ''
    if type == 'public':
        conference = source[1]
        nickname_to = body

        if not gLoaded:
            init(conference)

        if len(nickname_to.strip()) == 0:
            message = 'Забыл указать ник нового юзера'
            reply(type, source, message)
            return
        else:
            jid_to = handler_jid(conference + '/' + nickname_to)

        logging.debug(jid_to)
        if _get_main_jid(jid_to, conference) is not None:
            message = 'Пользователь с таким JID уже зарегистрирован'
        elif _get_main_nickname(nickname_to, conference) is not None:
            message = 'Пользователь с таким никнеймом уже зарегистрирован'
        else:
            gUsers[conference][nickname_to] = jid_to
            gProfiles[conference][jid_to] = {}
            for entity_type in gEntities.keys():
                gProfiles[conference][jid_to][entity_type] = 0

            gJids[conference][jid_to] = [jid_to] # ?
            gAliases[conference][nickname_to] = [nickname_to] # ?
            _save_profiles(conference)
            message = 'Ok'
    else:
        message = 'Только в конференции.'

    reply(type, source, message)

def handler_top(type, source, body):
    global gProfiles, gEntities, LOISES

    if type == 'public':
        conference = source[1]

        limit, entity_type = 10, LOISES
        for v in body.split(' '):
            if re.match(r'\d+', v):
                limit = int(v)
            for ent_k, ent_v in gEntities.iteritems():
                if ent_v == v.title():
                    entity_type = ent_k
                    break

        if not gLoaded:
            init(conference)

        i, top_list = 0, {}
        for jid, values in gProfiles[conference].items():
            i += 1
            if i >= limit:
                break
            if values.has_key(entity_type):
                top_list[values['aliases'][0]] = values[entity_type]

        i, message = 1, ''
        for nickname, value in dict(sorted(top_list.items(), key=operator.itemgetter(1))).items():
            message += '%d. %s (%d)\n' % (i, nickname, value)
            i += 1
    else:
        message = 'Только в конференции.'

    reply(type, source, message)

def handler_profile(type, source, body):
    global gProfiles, gEntities

    if type == 'public':
        conference = source[1]
        nickname_from = source[2]
        nickname_to = body

        if not gLoaded:
            init(conference)

        if len(nickname_to.strip()) == 0:
            jid_main_to = _get_main_jid_by_nickname(nickname_from, conference)
        else:
            jid_main_to = _get_main_jid_by_nickname(nickname_to, conference)

        logging.debug(nickname_to)
        logging.debug(len(nickname_to.strip()) == 0)
        logging.debug(jid_main_to)
        message = ''
        if jid_main_to is None or not gProfiles.has_key(conference) or not gProfiles[conference].has_key(jid_main_to):
            message = 'Не зарегистрирован.'
        else:
            for k, v in gEntities.items():
                if not gProfiles[conference][jid_main_to].has_key(k):
                    value = 0
                else:
                    value = gProfiles[conference][jid_main_to][k]
                message += v + ': %d, ' % value
            message = message[:-2] # отрезаем запятую с пробелом в конце
    else:
        message = 'Только в конференции.'

    reply(type, source, message)

def _get_main_nickname(nickname, conference):
    """
    Найти и вернуть главный никнейм по никнейму или алиасу.
    """
    global gAliases, gUsers

    result = None
    if gUsers.has_key(conference) and nickname in gUsers[conference].keys():
        result = nickname

    if result is None and gAliases.has_key(conference):
        for main_nickname, aliases_list in gAliases[conference].items():
            if nickname in aliases_list:
                result = main_nickname

    return result

def _get_main_jid(jid, conference):
    """
    Найти и вернуть главный JID по никнейму или алиасу.
    """
    global gJids, gUsers

    result = None
    if gUsers.has_key(conference) and jid in gUsers[conference].values():
        result = jid

    if result is None and gJids.has_key(conference):
        for main_jid, jid_list in gJids[conference].items():
            if jid in jid_list:
                result = main_jid

    return result

def _get_main_jid_by_nickname(nickname, conference):
    """
    Найти и вернуть главный JID по никнейму или алиасу.
    """
    global gJids, gUsers

    result = None
    nickname = _get_main_nickname(nickname, conference)
    if gUsers.has_key(conference) and nickname in gUsers[conference].keys():
        result = gUsers[conference][nickname]

    return result

def _add_entity(entity_type, type, source, body):
    global gProfiles, gJids, gEntities, GROUPCHATS

    message = ''
    if type == 'public':
        conference = source[1]
        nickname_from = source[2]
        nickname_to = body
        nickname_main_to = _get_main_nickname(nickname_to, conference)
        if nickname_main_to is not None:
            jid_to = handler_jid(conference + '/' + nickname_main_to)
        else:
            jid_to = handler_jid(conference + '/' + nickname_to)
        jid_main_to = _get_main_jid(jid_to, conference)

        if not gLoaded:
            init(conference)

        if not gProfiles.has_key(conference):
            gProfiles[conference] = {}
            gJids[conference] = {}

        if nickname_to != nickname_from and nickname_main_to != _get_main_nickname(nickname_from, conference):
            if nickname_to in GROUPCHATS[conference] or nickname_main_to in GROUPCHATS[conference]:
                if not gProfiles[conference].has_key(jid_to):
                    gProfiles[conference][jid_to] = {'jids': [jid_to], 'aliases': [nickname_to], entity_type: 1}
                    for ent_t in gEntities.keys():
                        if entity_type != ent_t:
                            gProfiles[conference][jid_to][ent_t] = 0

                    gJids[conference][nickname_to] = [jid_to]
                else:
                    if not gProfiles[conference][jid_to].get(entity_type):
                        gProfiles[conference][jid_to][entity_type] = 0

                    gProfiles[conference][jid_to][entity_type] += 1
                    _save_profiles(conference)

                message = 'Ok'
            # else:
            #     message = 'Пользователь «{0}» в комнате отсутствует.'.format(nickname_to)
        else:
            message = 'Голосования за себя не учитываются.'
    else:
        message = 'Только в конференции.'

    if len(message) > 0:
        reply(type, source, message)

    logging.debug(gProfiles)
    logging.debug(gJids)

def init(conference):
    global gProfiles, gLoaded, gJids, gAliases, gUsers

    file = 'dynamic/' + conference + '/profiles.txt'
    if initialize_file(file):
        try:
            fcontent = eval(read_file(file))
            gProfiles[conference] = fcontent.get('gProfiles', {})
            gJids[conference] = fcontent.get('gJids', {})
            gUsers[conference] = fcontent.get('gUsers', {})
            gAliases[conference] = fcontent.get('gAliases', {})
            gLoaded = True
            logging.debug('init')
        except:
            Print('Не удалось прочитать список профилей.', color1)
            lytic_crashlog(read_file)
    else:
        Print("\n\nError: невозможно подгрузить файл " + file, color2)

def _save_profiles(conference = ''):
    global gProfiles, gJids, gUsers, gAliases

    if conference == '':
        for conference in gProfiles.keys():
            write_file('dynamic/' + conference + '/profiles.txt', str(
                {
                    'gProfiles': gProfiles[conference],
                    'gJids':     gJids[conference],
                    'gUsers':    gUsers[conference],
                    'gAliases':  gAliases[conference]
                 }
            ))
    else:
        write_file('dynamic/' + conference + '/profiles.txt', str(
            {
                'gProfiles': gProfiles[conference],
                'gJids':     gJids[conference],
                'gUsers':    gUsers[conference],
                'gAliases':  gAliases[conference]
             }
        ))


handler_register("01si", init)
command_handler(handler_profile, 10, "profile")
command_handler(handler_top, 10, "profile")
command_handler(handler_add_router, 20, "profile")

for entity_type in gEntities.keys():
    exec('''def handler_{0}(type, source, body): _add_entity('{0}', type, source, body)'''.format(entity_type))
    command_handler_custom(locals()['handler_{0}'.format(entity_type)], 10, "profile")