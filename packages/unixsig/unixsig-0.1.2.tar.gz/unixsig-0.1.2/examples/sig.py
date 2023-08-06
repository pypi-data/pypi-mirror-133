# MIT License
#
# Copyright (c) 2021 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import signal
import time
import sys

from unixsig.listener import Listener


# Run the following to kill the process
# kill -15 $ID
if __name__ == '__main__':
    x = Listener()

    print('Process ID:', x.getpid())

    # Wait in an endless loop for signals
    while True:
        print('Running long process ...')
        time.sleep(3)
        print('Long process finished ...')

        if x.is_received(signal.SIGTERM):
            print('(SIGTERM) terminating the process')
            print('(SIGTERM) Doing some cleanup')
            time.sleep(3)

            x.discard(signal.SIGTERM)
            sys.exit()

        if x.is_received(signal.SIGINT):
            print('(SIGINT) terminating the process')
            print('(SIGINT) Doing some cleanup')
            time.sleep(3)

            x.discard(signal.SIGINT)
            sys.exit()
