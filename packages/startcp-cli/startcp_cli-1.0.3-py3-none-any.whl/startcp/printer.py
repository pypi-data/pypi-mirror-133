from halo import Halo

import os
import platform
import colorama


class Rangebi:
    # colour constants
    # Issue#6 temparary printing in white for windows
    if platform.system() == 'Windows':
        colorama.init()

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    spinner = None

    def get_in_danger(self, message):
        return Rangebi.FAIL + str(message) + Rangebi.ENDC

    def get_in_warning(self, message):
        return Rangebi.WARNING + str(message) + Rangebi.ENDC

    def get_in_bold(self, message):
        return Rangebi.BOLD + str(message) + Rangebi.ENDC

    def get_in_success(self, message):
        return Rangebi.OKGREEN + str(message) + Rangebi.ENDC

    def get_in_info(self, message):
        return Rangebi.OKBLUE + str(message) + Rangebi.ENDC

    def set_spinner(self):
        self.spinner = Halo(text='preparing battlespace...', spinner='dots')

    def start_spinner(self):
        self.spinner.start()

    def stop_spinner(self):
        self.spinner.stop()

    def clear_spinner(self):
        self.spinner = None


def new_lines(count=1):
    for i in range(count):
        print("")


def get_tab(count=1):
    for i in range(count):
        print("\t")


def get_dashed_lines(count=1):
    rangebi = Rangebi()
    for i in range(count):
        if i == count - 1 and count != 1:
            print(
                rangebi.get_in_warning(
                    ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
                ),
                end=""
            )
        else:
            print(
                rangebi.get_in_warning(
                    ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
                ),
            )


def print_start_cp_credits():
    rangebi = Rangebi()
    print(
        rangebi.get_in_info("## Credits :")
    )
    new_lines()
    print(
        rangebi.get_in_warning("- MIT Licensed")
    )
    new_lines()
    print(
        "- Contributors :"
    )
    print(
        "\t\t- ",
        rangebi.get_in_success(
            "Sujit (https://github.com/sujitdhond142)"
        )
    )
    new_lines()
    print(
        "\t\t- ",
        rangebi.get_in_success(
            "Ankush (https://github.com/asprazz)"
        )
    )
    new_lines()


def print_menu():
    rangebi = Rangebi()

    get_help_option_text(
        "cp $competition_url"
    )
    print("\t\t-- to build battlespace for the competition")
    new_lines()
    print("\t\t-- eg. cp https://www.codechef.com/NOV21B, cp codechef.com/NOV21B, cp codechef/NOV21b ")
    print("\t\t-- eg. cp https://www.codeforces.com/1616, cp codeforces.com/contest/1616, cp codeforces/1616 ")

    new_lines()

    get_help_option_text(
        "g or generate"
    )
    print("\t\t-- to toggle generatition of configuration file")

    get_help_option_text(
        "v or vw or vc or viewconfig"
    )
    print("\t\t-- to toggle view of configuration file")


    new_lines()

    get_help_option_text(
        "h or help"
    )
    print("\t\t-- to print this help")

    new_lines()

    get_help_option_text(
        "q or e or exit or quit"
    )
    print("\t\t-- exit from the program")



def get_help_option_text(option_text):
    rangebi = Rangebi()
    print(
        rangebi.get_in_warning(
            "(StartCP) $"
        ),
        end=" "
    )

    print(
        rangebi.get_in_info(
            option_text
        )
    )


def print_header():
    rangebi = Rangebi()

    logo = """
::                                                                                      ::
::            ____ _____  _    ____ _____ ____ ____        ____ _     ___               ::
::           / ___|_   _|/ \  |  _ \_   _/ ___|  _ \      / ___| |   |_ _|              ::
::           \___ \ | | / _ \ | |_) || || |   | |_) |____| |   | |    | |               ::
::            ___) || |/ ___ \|  _ < | || |___|  __/_____| |___| |___ | |               ::
::           |____/ |_/_/   \_\_| \_\|_| \____|_|         \____|_____|___|              ::
::                                                                                      ::
    """
    print("")
    print(
        rangebi.get_in_bold(
            rangebi.get_in_success(
                logo
            )
        )
    )
