from pxpip.classes import CommandFactory


def exec(p_args):
    stripped_args = p_args[1:]  # removes init argument
    CommandFactory.get_command_class(stripped_args).run()

