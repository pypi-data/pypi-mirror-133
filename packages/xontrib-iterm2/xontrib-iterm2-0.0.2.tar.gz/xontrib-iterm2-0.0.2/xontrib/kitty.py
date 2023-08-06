import sys
from xonsh.built_ins import XSH


def kitty_esc(code):
    return f"\x1b\x5d133;{code}\x1b\x5c"


def write_esc(code):

    sys.stdout.write(kitty_esc(code))
    sys.stdout.flush()


# Inform iTerm2 that command starts here
@XSH.builtins.events.on_pre_prompt
def kitty_pre_prompt(cmd=None):
    """write before starting to print out the prompt"""
    write_esc("A")


@XSH.builtins.events.on_precommand
def kitty_preout(cmd=None):
    """write before starting to print out the output from the command"""
    write_esc("C")
