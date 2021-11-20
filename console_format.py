class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[38;5;35m'
    WARNING = '\033[93m'
    ERROR = "\033[31;4m"
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ok(text):
    return Colors.OKGREEN + text + Colors.ENDC


def error(text):
    return Colors.ERROR + text + Colors.ENDC
