
from classes.util import is_blank, is_not_blank
from plugin_manager import Plugin_Manager
from plugins.speaker.speaker import Speaker

print("Instanciando Plugin Manager.")
manager = Plugin_Manager()

print("Carregando plugins.")
manager.setup_plugin_manager()

speaker = manager.get_plugin_class_by_name("Speaker", "Internal")
speaker.speak("Iniciando assistente Beth. Diga Beth para acionar a assistente.")

core = manager.get_plugin_class_by_name("Core", "Internal")
core.adjust_threshold()

while core.is_it_exiting is False:

    # Beth speaks a message.
    speaker.speak(manager.get_current_question())

    # User inputs a command.
    (input, error) = core.listen()

    # Some error occurred.
    if is_not_blank(error):
        speaker.speak(error)
        continue

    # Next input from the user.
    if is_blank(input):
        continue

    # Beth speaks what the user said.
    speaker.speak_what_i_say(input)

    # Beth processes the user's command.
    output = core.run(input)

    # Processing message from Beth's core.
    if is_not_blank(output) is True:
        # next input from the user.
        if core.is_it_exiting:
            speaker.speak(output)
            continue

        # waiting mode activate.
        if core.is_it_waiting is True:
            speaker.speak(output)
            speaker.activated = False
            continue

        # waiting mode deactivate.
        if core.is_it_waiting is False:
            speaker.activated = True
            speaker.speak(output)
            continue

    # process command by plugins.
    output = manager.run_plugins(input)
    if output is not None:
        speaker.speak(output)
