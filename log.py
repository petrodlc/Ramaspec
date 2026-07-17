__all__ = [
    'log',
]


import time
import copy
import re


class log:
    __ANSI_esc = {
        'reset': 0,
        'bold': 1,
        'faint': 2,
        'italic': 3,
        'underline': 4,
        'blink': 5,
        'inverse': 7,
        'hidden': 8,
        'strikethrough': 9,
        'reset_bold': 22,
        'reset_faint': 22,
        'reset_italic': 23,
        'reset_undeline': 24,
        'reset_blink': 25,
        'reset_inverse': 27,
        'reset_hidden': 28,
        'reset_strikethrough': 29,
        # COLORS
        'fg_black': 30,
        'fg_red': 31,
        'fg_green': 32,
        'fg_yellow': 33,
        'fg_blue': 34,
        'fg_magenta': 35,
        'fg_cyan': 36,
        'fg_white': 37,
        'fg_default': 39,
        'fg_reset': 0,

        'bg_black': 40,
        'bg_red': 41,
        'bg_green': 42,
        'bg_yellow': 43,
        'bg_blue': 44,
        'bg_magenta': 45,
        'bg_cyan': 46,
        'bg_white': 47,
        'bg_default': 49,
        'bg_reset': 0,

        'fg_br_black': 90,
        'fg_br_red': 91,
        'fg_br_green': 92,
        'fg_br_yellow': 93,
        'fg_br_blue': 94,
        'fg_br_magenta': 95,
        'fg_br_cyan': 96,
        'fg_br_white': 97,

        'bg_br_black': 100,
        'bg_br_red': 101,
        'bg_br_green': 102,
        'bg_br_yellow': 103,
        'bg_br_blue': 104,
        'bg_br_magenta': 105,
        'bg_br_cyan': 106,
        'bg_br_white': 107,
    }

    def __init__(self, log_level: int = 1):
        self.level = log_level
        self.__events = []
        self.info('Log instance initialized')
        return

    @property
    def events(self):
        events = copy.deepcopy(self.__events)
        for ev in events:
            ev[-1] = re.sub('\\x1b\\[.*?m', '', ev[-1])
        return events

    @property
    def styles(self):
        return self.__ANSI_esc.keys()

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level: int):
        self.__level = max(-1, level)
        return

    @level.deleter
    def level(self):
        self.__level = 1
        return

    def print_events(self, log_level: int = None):
        if log_level is None:
            log_level = self.__level
        for ev in self.__events:
            if ev[1] <= log_level:
                print(f'{ev[0]}: {ev[-1]}')
        return

    def print_styles(self):
        for style in self.__ANSI_esc.keys():
            print(self.esc(style) + style + self.esc('reset'))
        return

    def esc(self, *args):
        sequence = '\x1b['
        for arg in args:
            if arg in self.__ANSI_esc.keys():
                sequence += f'{self.__ANSI_esc[arg]:d};'
            else:
                self.warning(f'{arg} is not a valid style identifier.')
        return sequence + 'm'

    def log(self,
            msg: str,
            keyword: str,
            style: list(str) = [],
            keyword_style: list(str) = [],
            log_level: int = 2):
        full_msg = self.esc(*style) \
            + '[' \
            + self.esc('reset', *keyword_style) \
            + keyword.center(9).upper() \
            + self.esc('reset', *style) \
            + ']> ' \
            + self.esc('reset') \
            + msg

        log_level = max(0, log_level)

        self.__events.append([time.monotonic_ns(), log_level, full_msg])
        if log_level <= self.__level:
            print(full_msg)
        return

    def error(self, msg):
        self.log(msg,
                 'error',
                 ['bold'],
                 ['bold',
                  'fg_br_red'],
                 log_level=0)
        return

    def warning(self, msg):
        self.log(msg,
                 'warning',
                 ['bold'],
                 ['bold', 'fg_br_yellow'],
                 log_level=1)
        return

    def info(self, msg):
        self.log(msg,
                 'log',
                 ['bold'],
                 ['bold', 'fg_br_blue'],
                 log_level=2)
        return

    def debug(self, msg):
        self.log(msg,
                 'debug',
                 ['bold'],
                 ['bold', 'fg_magenta'],
                 log_level=3)
        return
