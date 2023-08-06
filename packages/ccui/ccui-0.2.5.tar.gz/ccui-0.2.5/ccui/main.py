"""
The main interaction console of CCUI
"""

from cmd import Cmd
from rich import print as rprint


# CCUI Modules
from ccui.constants import (
    LINUX,
    WINDOWS,
)
from ccui.errors import (
    ExitCCUIRestart,
    ExitCCUIShutdown,
    ExitCCUIReload,
)
import ccui.util


class CCUIPrompt(Cmd):
    def do_help(self, args: str) -> None:
        """
        help

        Description:
            Provides all of CCUI commands.

        Parameter List:
            command - Displays help for specific given command.
        """
        if args.strip():
            return print("  Usage: help (no arguments)")
        ccui.util.output_file_content('ccui_prompt_help.txt')
        

    def do_man(self, command: str) -> None:
        """
        man [command]

        Description:
            Provides a manual for given command.

        Parameter List:
            command - Displays manual for specific given command.
        """
        if not command.strip():
            return print(' Usage: man [command]')
        try:
            print(getattr(self, "do_" + command).__doc__)
        except AttributeError:
            rprint(f"[#E74856]ERROR: No such command '{command}'[/#E74856]")


    def do_restart(self, args: str) -> None:
        """
        restart

        Description:
            A complete restart of CCUI to update code changes.
        """
        if args.strip():
            return print("  Usage: restart (no arguments)")
        raise ExitCCUIRestart

    
    def do_shutdown(self, args: str) -> None:
        """
        shutdown

        Description:
            Shuts down CCUI.
        """
        if args.strip():
            return print("  Usage: shutdown (no arguments)")
        raise ExitCCUIShutdown


    def do_reload(self, args: str):
        """
        reload

        Description:
            Reloads CCUI.
        """
        if args.strip():
            return print("  Usage: reload (no arguments)")
        raise ExitCCUIReload


    def do_clear(self, args: str) -> None:
        """
        clear

        Description:
            Clears the terminal.
        """
        if args.strip():
            return print("  Usage: clear (no arguments)")
        ccui.util.clear()


    def do_tools(self, args: str) -> None:
        """
        tools

        Description:
            Shows available tools.
        """
        if args.strip():
            return print("  Usage: tools (no arguments)")
        ccui.util.output_file_content('ccui_tools.txt')


    # -Alternative names for commands-
    # do_ is an identifier for commands
    do_commands = do_help
    do_reboot = do_restart
    do_exit = do_quit = do_shutdown
    do_refresh = do_reload
    do_cls = do_clear


def launch(fresh_launch: bool = True) -> None:
    """
    Handles the CCUI initial prompt, Prevents KeyboardInterrupt.

    Keyword arguments:
    fresh_launch -- set default prompt (default True)
    """
    while True:
        try:
            if fresh_launch:
                ccui.util.clear()
                prompt = CCUIPrompt()
                prompt.prompt = "[CCUI] >> "
                prompt.cmdloop(ccui.util.output_file_content("ccui_logo.txt", "*", "CCUI"))
            else:
                prompt.cmdloop()
        except KeyboardInterrupt:
            print("^C")
            fresh_launch = False


if __name__ == '__main__':
    launch()
