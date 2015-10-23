# /* coding: utf-8 */

from traceback import print_exc
from BlackSmith import COMMANDS, COMMAND_HANDLERS, COMMSTAT, Print, read_file, color2
import six
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

'''
    Делает то же самое, что стандартный command_handler, но в файле help можно прописать список команд `cmd`,
    вместо одного элемента. Некое подобие алиасов.

    Как использовать:
        execfile("imports/command_handler_custom.py") # подгружаем кастомный обработчик
        command_handler_custom(handler_vanguy, 10, "vanguy") # вместо command_handler, вызываем наш обработчик
'''
def command_handler_custom(instance, access = 0, plug = "default"):
    commands = []
    try:
        commands = eval(read_file("help/%s" % plug).decode('utf-8'))[instance.func_name]["cmd"]
        if isinstance(commands, six.string_types):
            commands = [commands]
    except:
        print_exc()
        command = instance.func_name.lower()
        Print("\nPlugin \"%s\" has no help and command name. New command name: %s." % (plug, command), color2)

    for command in commands:
        # logging.debug(command)
        if COMMANDS.get(command) or COMMAND_HANDLERS.get(command):
            if plug != COMMANDS[command].get("plug"):
                Print("\nCommands in \"%s\" and \"%s\" are repeated." % (plug, COMMANDS[command].get("plug")), color2)
                command += "1"
        if command not in COMMSTAT:
            COMMSTAT[command] = {'col': 0, 'users': []}
        COMMAND_HANDLERS[command] = instance
        COMMANDS[command] = {'plug': plug, 'access': access}