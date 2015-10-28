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

# {'conf@cjr': {''}}
gProfiles = {}
gAliases = {}
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

def handler_add_alias(type, source, body):
    pass

def handler_add_jid(type, source, body):
    pass

def handler_top(type, source, body):
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
    if type == 'public':
        conference = source[1]
        nickname_from = source[2]
        nickname_to = body

        if not gLoaded:
            init(conference)

        if len(nickname_to) == 0:
            jid_to = handler_jid(conference + '/' + nickname_from)
        else:
            jid_to = handler_jid(conference + '/' + nickname_to)

        message = ''
        for k, v in gEntities.items():
            if not gProfiles.has_key(conference) or not gProfiles[conference].has_key(jid_to) or not gProfiles[conference][jid_to].has_key(k):
                value = 0
            else:
                value = gProfiles[conference][jid_to][k]
            message += v + ': %d, ' % value
        message = message[:-2] # отрезаем запятую с пробелом в конце
    else:
        message = 'Только в конференции.'

    reply(type, source, message)

def _add_entity(entity_type, type, source, body):
    message = ''
    if type == 'public':
        conference = source[1]
        nickname_from = source[2]
        nickname_to = body
        jid_to = handler_jid(conference + '/' + nickname_to)

        if not gLoaded:
            init(conference)

        if not gProfiles.has_key(conference):
            gProfiles[conference] = {}
            gJids[conference] = {}

        if nickname_to != nickname_from:

            if nickname_to in GROUPCHATS[conference]:
                if not gProfiles[conference].has_key(jid_to) or nickname_to not in gProfiles[conference][jid_to].get('aliases'):
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

                message = 'Ок.'
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
    global gProfiles, gLoaded

    file = 'dynamic/' + conference + '/profiles.txt'
    gLoaded = True
    if initialize_file(file):
        try:
            fcontent = eval(read_file(file))
            gProfiles[conference] = fcontent.get('gProfiles')
            gJids[conference] = fcontent.get('gJids')
            logging.debug('init')
        except:
            Print('Не удалось прочитать список профилей.', color1)
            lytic_crashlog(read_file)

def _save_profiles(conference = ''):
    global gProfiles
    filename = 'dynamic/' + conference + '/profiles.txt'
    if conference == '':
        for conference in gProfiles:
            write_file(filename, str({'gProfiles': gProfiles[conference], 'gJids': gJids[conference]}))
    else:
        write_file(filename, str({'gProfiles': gProfiles[conference], 'gJids': gJids[conference]}))


handler_register("01si", init)
command_handler(handler_profile, 10, "profile")
command_handler(handler_top, 10, "profile")

for entity_type in gEntities.keys():
    exec('''def handler_{0}(type, source, body): _add_entity('{0}', type, source, body)'''.format(entity_type))
    command_handler_custom(locals()['handler_{0}'.format(entity_type)], 10, "profile")