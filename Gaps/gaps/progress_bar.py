import sys


def print_progress(
    iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 2, bar_length: int = 50
):
    ''' Call in a loop to create terminal progress bar'''
    percents = '{{0:.{}f}}'.format(decimals).format(100 * (iteration / total))
    filled_length = int(round(bar_length * iteration / total))
    bar = '\033[32m{0}\033[0m\033[31m{1}\033[0m'.format('█' * filled_length, '-' * (bar_length - filled_length))

    sys.stdout.write('\r{0: <16} {1} {2}% {3}'.format(prefix, bar, percents, suffix))

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
