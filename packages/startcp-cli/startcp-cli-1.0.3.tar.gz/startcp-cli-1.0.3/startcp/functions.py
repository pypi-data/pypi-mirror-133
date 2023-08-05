import json
import requests
import re
import os
from pathlib import Path
import datetime

from dotenv import load_dotenv, find_dotenv

try:
    import printer
    import constants
    import builder
    import version
    import logger
except Exception:
    from startcp import printer, constants, builder, version, logger


rangebi = printer.Rangebi()
logger = logger.Logger()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    if constants.startcp_config_file.is_file():
        load_dotenv(dotenv_path=str(constants.startcp_config_file))
    else:
        load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
except Exception:
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
    print(rangebi.get_in_info(
        "Custom configuration file not loaded. Please fix the file first."))


def run(args):

    printer.print_header()

    if args.generate:
        generate_start_cp_config_file()
        return
    elif args.version:
        print_version_info()
        return

    operate(args)


def operate(args):
    comp_url = ""

    if args.url:
        comp_url = args.url.lower()
    else:
        printer.new_lines(1)
        printer.print_menu()
        printer.new_lines(1)
        while (True):
            print(
                rangebi.get_in_warning(
                    "(StartCP) $"
                ),
                end=" "
            )
            choices = input().split(" ")

            if choices[0].lower() in ["h", "hlp", "help", "hl"]:
                printer.print_menu()
                print("")
            elif choices[0].lower() in ["e", "exit", "ext", "q", "qt", "quit"]:
                break
            elif choices[0].lower() in ["c", "clr", "clear", "clrscr"]:
                print("clear screen implementation in progress")
            elif choices[0].lower() in ["cp", "comp", "build", "b"]:
                if len(choices) == 1:
                    print(
                        rangebi.get_in_danger(
                            "Please give url as second paramter. eg. cp codechef/COMP_ID")
                    )
                    continue
                if builder.perform_build(choices[1].strip()):
                    print(
                        rangebi.get_in_success(
                            "Successfully prepared for code battle. Good luck!"
                        )
                    )
            elif choices[0].lower() in ["g", "gen", "generate"]:
                generate_start_cp_config_file()
                break
            elif choices[0].lower() in ["v", "vc", "vw", "view", "viewconfig"]:
                view_start_cp_config_file()
            else:
                print("Invalid command. Please use h or help for more info.")


def generate_start_cp_config_file():
    # TODO: Move this to a own generator module
    print("Generating startcp config file...")

    IS_SETUP_DONE = None
    PROJECT_PATH = None
    USE_TEMPLATE = None
    MAIN_LANG_TEMPLATE_PATH = None
    BACKUP_LANG_TEMPLATE_PATH = None
    SEPERATE_FOLDER_STRUCTURE_FOR_DIFFERENT_SITES = 1
    CODECHEF_FOLDER_NAME = "Codechef"
    CODEFORCES_FOLDER_NAME = "Codeforces"
    PRACTICE_FOLDER_NAME = "Practice"
    AFTER_GENERATION_COMMAND = None

    while (True):
        print("Do you want to use custom project path? (y/n): ", end="")
        choice = input().lower().strip()
        if choice in ["y", "yes"]:
            IS_SETUP_DONE = 1
            break
        elif choice in ["n", "no"]:
            IS_SETUP_DONE = 0
            break
        else:
            print("Invalid input. Please use y or n.")

    if IS_SETUP_DONE == 1:
        while (True):
            print("Enter project path: ", end="")
            PROJECT_PATH = input().strip()
            if os.path.isdir(PROJECT_PATH):
                break
            else:
                print("Invalid path. Please try again.")

    while (True):
        print("Do you want to use custom template? (y/n): ", end="")
        choice = input().lower().strip()
        if choice in ["y", "yes"]:
            USE_TEMPLATE = 1
            break
        elif choice in ["n", "no"]:
            USE_TEMPLATE = 0
            break
        else:
            print("Invalid input. Please use y or n.")

    if USE_TEMPLATE == 1:
        while (True):
            print("Enter main language template path: ", end="")
            MAIN_LANG_TEMPLATE_PATH = input().strip()
            if Path(MAIN_LANG_TEMPLATE_PATH).is_file():
                break
            else:
                print("Invalid path. Please try again.")

        while (True):
            print("Enter backup language template path: ", end="")
            BACKUP_LANG_TEMPLATE_PATH = input().strip()
            if Path(BACKUP_LANG_TEMPLATE_PATH).is_file():
                break
            else:
                print("Invalid path. Please try again.")

    while (True):
        print("Do you want to run command after generation? (y/n): ", end="")
        choice = input().lower().strip()
        if choice in ["y", "yes"]:
            print("Enter command: ", end="")
            AFTER_GENERATION_COMMAND = input().strip()
            break
        elif choice in ["n", "no"]:
            AFTER_GENERATION_COMMAND = 0
            break
        else:
            print("Invalid input. Please use y or n.")

    start_cp_configuration = """IS_SETUP_DONE = {IS_SETUP_DONE}
PROJECT_PATH = {PROJECT_PATH}
USE_TEMPLATE = {USE_TEMPLATE}
MAIN_LANG_TEMPLATE_PATH = {MAIN_LANG_TEMPLATE_PATH}
BACKUP_LANG_TEMPLATE_PATH = {BACKUP_LANG_TEMPLATE_PATH}
SEPERATE_FOLDER_STRUCTURE_FOR_DIFFERENT_SITES = {SEPERATE_FOLDER_STRUCTURE_FOR_DIFFERENT_SITES}
CODECHEF_FOLDER_NAME = {CODECHEF_FOLDER_NAME}
CODEFORCES_FOLDER_NAME = {CODEFORCES_FOLDER_NAME}
PRACTICE_FOLDER_NAME = {PRACTICE_FOLDER_NAME}
AFTER_GENERATION_COMMAND = {AFTER_GENERATION_COMMAND}""".format(
        IS_SETUP_DONE=IS_SETUP_DONE,
        PROJECT_PATH=PROJECT_PATH,
        USE_TEMPLATE=USE_TEMPLATE,
        MAIN_LANG_TEMPLATE_PATH=MAIN_LANG_TEMPLATE_PATH,
        BACKUP_LANG_TEMPLATE_PATH=BACKUP_LANG_TEMPLATE_PATH,
        SEPERATE_FOLDER_STRUCTURE_FOR_DIFFERENT_SITES=SEPERATE_FOLDER_STRUCTURE_FOR_DIFFERENT_SITES,
        CODECHEF_FOLDER_NAME=CODECHEF_FOLDER_NAME,
        CODEFORCES_FOLDER_NAME=CODEFORCES_FOLDER_NAME,
        PRACTICE_FOLDER_NAME=PRACTICE_FOLDER_NAME,
        AFTER_GENERATION_COMMAND=AFTER_GENERATION_COMMAND
    )

    os.makedirs(constants.startcp_default_folder, exist_ok=True)
    logger.info("Generating default config folder: " +
                constants.startcp_default_folder + " if not exists")
    with open(str(constants.startcp_config_file), "w") as f:
        f.write(start_cp_configuration)
        logger.info("Generating default config file: " +
                    str(constants.startcp_config_file) + " if not exists")
    print("Successfully generated startcp config file. Please restart the application.")


def view_start_cp_config_file():
    # TODO: Move this to a own generator module

    print("Viewing startcp config file...")
    printer.new_lines()
    if os.path.isfile(str(constants.startcp_config_file)):
        with open(str(constants.startcp_config_file), "r") as f:
            print(f.read())
    else:
        print("No startcp config file found.")


def print_version_info():
    print(
        "startcp-cli current version:{version_string}".format(version_string=version.string()))
