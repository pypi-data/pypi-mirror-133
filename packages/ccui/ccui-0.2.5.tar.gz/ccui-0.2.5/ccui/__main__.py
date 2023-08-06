import importlib
import ccui.main
from ccui.main import launch
from ccui.errors import (
    ExitCCUIRestart,
    ExitCCUIShutdown,
    ExitCCUIReload,
)


def main():
    while True:
        try:
            launch()
        except ExitCCUIShutdown:
            break
        except ExitCCUIRestart:
            importlib.reload(ccui.main)
        except ExitCCUIReload:
            pass


if __name__ == '__main__':
    main()
