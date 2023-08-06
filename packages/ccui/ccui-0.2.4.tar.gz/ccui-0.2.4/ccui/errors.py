"""
CCUI's Error Codes
"""

# --Launch related errors--
class ExitCCUIRestart(Exception):
    pass


class ExitCCUIShutdown(Exception):
    pass


class ExitCCUIReload(Exception):
    pass

# ----