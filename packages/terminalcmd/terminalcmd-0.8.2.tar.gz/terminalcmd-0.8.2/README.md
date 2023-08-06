# terminalcmd

**`Terminalcmd`** is a Python library which can help you to 
make your own terminal program with high-intellegence instruments, 
that will make your code "clear" and readable.

`Note`: Library is in beta-test now, so it will update very often.

# Installition
###### Using Pypi:
```bash
$ pip install terminalcmd
```
## Examples of base instruments:
##### Object stream:
```py
# Working like printing (not FULL) iterator:
my_list = [1, 2, 3]
terminalcmd.log(f"Maybe we need to see subobjects of {my_list}?")
terminalcmd.stream(my_list)
```
##### Iterator:
```py
# iter(callable) example:
terminalcmd.citer([1, 2, 3])

# iter(callable, sentinel) example:
terminalcmd.log("Now let's see how it work with `terminalcmd.prompt()` and 'stop' as sentinel")
terminalcmd.citer(terminalcmd.prompt, "stop")
```
##### Clearing console:
```py
if terminalcmd.prompt("Do you want to clear terminalcmd? (y/n): ").lower() == "y":
    terminalcmd.clear()
```
## Examples of BuilderCore (NOT ACTUAL MORE):
##### Easy-to-build greeter:
```py
from terminalcmd import (
    builder,  # To build your app you need this module.
    log,
    prompt
)


@builder.command(  # Decorator create commands.
    short_descrtiption="Greet you!",  # Set description, that will be shown in help-message.
    usage="greet (No arguments)"  # Let user know how to use this command.
                                  # Of course, all this params can be unfilled.
)
def greet() -> None:  # Create functiuon. As command name in console will be used function name.
    name = prompt("What's your name: ")  # Base input.
    log(f"Hello {name}!")  # Base log into console.


if __name__ == "__main__":
    builder.build()  # Start console.
```
##### Builtins:
```py
from terminalcmd import builder, log


@builder.command()  # Create some random command.
def hello() -> None:
    """Say "Hello!" to user."""
    log("hello!")


if __name__ == "__main__":
    builder.build()
```
If you'll run this file and type 'help', you'll see
that you have 3 commands: 'help', 'exit' and 'hello'.
But why? You added only one!
It's because of builtins commands:  

  Command `help` show all commands in your programm.
  Command `exit` kill current task with exit code 0.

If you need to get information about one command,
Use next syntax: `{command} ?`.
Let's see what will be after typing `help ?`:
```bash
>>> help ?

Command 'help':
  Description:
    'help' is a builtin command that show all commands in refactored case.
  Usage:
    'help' AND 'help ?'
```
Like this you can get info about every command.

Interest fact:
If you will call `builder.build()` without any
registred command in your file, you'll get
AttributeError (:
##### Some usefull things:
```py
from terminalcmd import (
    builder,
    log,
    color
)


@builder.command(
    short_descrtiption="Show usefull functions and methods.",
    usage="You can type whatever you want, but it must startswith 'show_uf'."
)
def show_uf() -> None:
    log(
        "\nLet's see commands arguments (like sys.argv, but in command):",
        builder.get_args(),
        sep="\n",
        end="\n\n"
    )
    curr_command = builder.get_command("show_uf")
    log(
        "If you need to work with some command use 'builder.get_command(command_name: str)'.",
        "Let's see description and usage of this command:",
        "Description: " + color.blue + curr_command.description,
        "Usage: " + color.blue + curr_command.usage,
        sep="\n",
        end="\n\n"
    )


if __name__ == "__main__":
    builder.build()
```
##### Customizing comandlet:
```py
from terminalcmd import builder, log


@builder.command()  # Create some random command.
def hello() -> None:
    """Say "Hello!" to user."""
    log("hello!")


if __name__ == "__main__":
    builder.build(
        comandlet="MaYbE_ChAnGe_CoMaNdLeT -|> ",   # Did you remember comandlet name in examples before?
                                                    # You can change it to your own text.
                                                    #
        notexist_text="THIS command is not exist."  # This text is optional and will be shown if user typed
                                                    # commands that not exist.
    )
```
Interest point:
If you need to have parameter `notexist_text` like:
`"This command {and_here_command_name} is not exist."`
Just add in text this phrase: `{command}`.
(but don't add \`f\` before text line) and library 
will replace this phrase with raised exception 
command name.
