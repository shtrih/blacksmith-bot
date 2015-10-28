# /* coding: utf-8 */

# from traceback import print_exc
# from BlackSmith import COMMANDS, COMMAND_HANDLERS, COMMSTAT, Print, read_file, color2
import six
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

'''
    Делает то же самое, что стандартный command_handler, но в файле help можно прописать список синонимов команды `cmd`: команда/синоним/еще_синоним.
    Некое подобие алиасов.

    Как использовать:
        execfile("imports/command_handler_custom.py") # подгружаем кастомный обработчик
        command_handler_custom(handler_vanguy, 10, "vanguy") # вместо command_handler, вызываем наш обработчик
'''
def command_handler_custom(instance, access = 0, plug = "default"):
    commands = []
    try:
        # «команда» или «команда/алиас_команды/еще_алиас» превращается в список команд
        commands = eval(read_file("help/%s" % plug))[instance.func_name]["cmd"].encode('utf-8').split('/')
        # чистим список от пустых элементов
        commands = filter(bool, map(str.strip, commands))
    except:
        print_exc()
        commands.append(instance.func_name.lower())
        Print("\nPlugin \"%s\" has no help and command name. New command name: %s." % (plug, commands[-1]), color2)

    for command in commands:
        # logging.debug(command)
        if COMMANDS.get(command):# or COMMAND_HANDLERS.get(command):
            if plug != COMMANDS[command].get("plug"):
                Print("\nCommands in \"%s\" and \"%s\" are repeated." % (plug, COMMANDS[command].get("plug")), color2)
                command += "1"
        if command not in COMMSTAT:
            COMMSTAT[command] = {'col': 0, 'users': []}
        COMMAND_HANDLERS[command] = instance
        COMMANDS[command] = {'plug': plug, 'access': access}