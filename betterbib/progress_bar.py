# -*- coding: utf8 -*-
#
import os


class ProgressBar(object):
    '''
    An ASCII art progress bar in the style of

    73% [==========================>          ] 143
    '''

    def __init__(self):
        # Determine progress bar width according to the current console width.
        rows, columns = os.popen('stty size', 'r').read().split()
        self._width = int(columns) - 10 - len(str(n))
        return

    def show(percentage):
        filled_width = int(percentage * progress_bar_width)
        empty_width = progress_bar_width - filled_width
        sys.stdout.write(('\r%3d%% [' + '=' * (filled_width - 1) + '>' +
                         ' ' * empty_width + '] %d')
                         % (int(100 * percentage), k)
                         )
        sys.stdout.flush()
        return
