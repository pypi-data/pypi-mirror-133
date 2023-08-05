# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Dallas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import (
    Any,
    Union,
    Optional
)

from .color_console import color


class commands:
    """Cotainer class, help to work with commands."""
    list = {  # Yes bad naming, but I've done all for user!)
        "help": [
            None,
            "Show all commands.",
            "'help' is a builtin command that show all commands in refactored case.",
            "'help' AND 'help ?'"
        ],
        "exit": [
            None,
            "Exit from app.",
            "'exit' is a builtin command that exit from current running app.",
            "'exit' AND 'exit ?'"
        ]
    }

    def __init__(self, command: str) -> None:
        self.command = command

    @property
    def short_description(self) -> str:
        """Return short command description."""
        return self.list[self.command][1]

    @property
    def description(self) -> str:
        """Return long command description."""
        return self.list[self.command][2]

    @property
    def usage(self) -> str:
        """Return command usage."""
        return self.list[self.command][3]

    @staticmethod
    def help_handler() -> None:
        """Reformat commands list and its methods meanings."""
        reformated_commands_list: str = ""
        name_length_list: list = [command for command in commands.list]
        desc_length_list: list = [commands(command).short_description for command in commands.list]

        name_length_list.sort(reverse=True, key=len)
        desc_length_list.sort(reverse=True, key=len)
        name_length_list: str = name_length_list[0]
        desc_length_list: str = desc_length_list[0]

        for command in commands.list:
            cmd = commands(command)
            first_spaces: str = " " * (len(name_length_list) - len(command))
            second_spaces: str = " " * (len(desc_length_list) - len(cmd.short_description))
            reformated_commands_list += f"{command}{first_spaces} | " \
                                        f"{cmd.short_description}{second_spaces} | " \
                                        f"{cmd.usage}\n"
        print("\n" + reformated_commands_list)

    @staticmethod
    def ask_handler(command: str) -> None:
        """Return information about given command."""
        cmd = commands(command)
        print(
            color.green  + "\n" + "Command '%s':"                    % command,
            color.magneta +       "  Short description:\n%s    %s"   % (color.reset, cmd.short_description),
            color.magneta +       "  Description:\n%s    %s"         % (color.reset, cmd.description),
            color.magneta +       "  Usage:\n%s    %s"               % (color.reset, cmd.usage) + color.reset,
            sep="\n",
            end="\n\n"
        )


def command(
    short_descrtiption: str = "Not added.",
    description: str = "Not added.",
    usage: str = "Not added."
) -> Any:
    """
    Commands decorator containing command parameters.

    :argument short_descrtiption: string Short info text, that will be shown in
    help command.
    :argument description: string Long info text that will be added as information how this
    command work and show in '{command} ?' menu.
    :argument usage: string Text that will be added as short example of command work.
    """
    def wrapper(function) -> None:
        """Decorator's wrapper containing function."""
        commands.list[function.__name__] = [function, short_descrtiption, description, usage]
    return wrapper


def get_command(command_name: str):
    """
    Return class commands with typed function.name.

    :argument command_name: string A name of command, that should be entered in class.
    """
    return commands(command_name)


last_args: list[str] = []


def get_args(argument_index: Optional[int] = None) -> Union[str, list]:
    """Return arguments entered in one line with LAST command."""
    if argument_index:
        return last_args[argument_index]
    return last_args


def build(
    comandlet: str = "betterconsole:/> ",
    notexist_text: str = color.red + "Unknown command." + color.reset
) -> None:
    """
    Command starting comandlet descriptor.

    :argument comandlet: string Text will be shown as a comandlet.
    :argument notexist_text: string Text will be shown if user typed
    not existing command.
    """
    while True:
        if len(commands.list) == 0:
            raise AttributeError("You have not added any commands.")
        try:
            input_line: list = input(comandlet).split(" ")
            print(color.reset, end="")  # Bad method.
            global last_args
            last_args.clear()
            last_args = input_line
            command: str = input_line[0]
            if command in commands.list:
                if len(input_line) > 1 and input_line[1] == "?":
                    commands.ask_handler(command)
                    continue
                match command:
                    case "help":
                        if commands.list["help"][0]:
                            commands.list["help"][0]()  # Expression is not callable.
                        else:
                            commands.help_handler()
                        continue
                    case "exit":
                        if commands.list["exit"][0]:
                            commands.list["exit"][0]()  # Expression is not callable.
                        else:
                            print("\n" + "Goodbye!")
                            exit(0)
                    case default:  # Local variable 'default' value is not used.
                        commands.list[command][0]()
            else:
                print("\n" + notexist_text.replace("{command}", command) + "\n")
        except Exception as exc:
            raise exc
