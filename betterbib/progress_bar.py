# -*- coding: utf8 -*-
#
import os
import sys

class ProgressBar(object):
    '''
    An ASCII art progress bar in the style of

    73% [==========================>          ] 143
    '''

    def __init__(self, total):
        # Determine progress bar width according to the current console width.
        rows, columns = os.popen('stty size', 'r').read().split()
        self._total = total
        self._width = int(columns) - 10 - len(str(total))
        return

    def show(self, k):
        percentage = float(k) / self._total
        filled_width = int(percentage * self._width)
        empty_width = self._width - filled_width
        sys.stdout.write(('\r%3d%% [' + '=' * (filled_width - 1) + '>' +
                         ' ' * empty_width + '] %d')
                         % (int(100 * percentage), k)
                         )
        sys.stdout.flush()
        return
