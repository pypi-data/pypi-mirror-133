import re
import os

try:
    import printer
    import constants
    import codechef
    import codeforces
    import logger

except Exception:
    from startcp import printer, constants, codechef, codeforces, logger



rangebi = printer.Rangebi()
logger = logger.Logger()

platform_id = None


def perform_build(comp_url):
    if not validate_url(comp_url):
        print(
            rangebi.get_in_danger(
                "Error orccured while validating url. Please try again!"
            )
        )
        printer.new_lines()
        logger.info("Error occured while validating url. Please try again! URL: " + comp_url)
        return False
    else:
        rangebi.set_spinner()
        rangebi.start_spinner()
        status = perform_operations_on_url(comp_url)
        rangebi.stop_spinner()
        rangebi.clear_spinner()
        return status


def validate_url(comp_url):
    global platform_id

    # regex matching for codechef url
    regex_validator = re.compile(constants.codechef_regex)
    if re.match(regex_validator, comp_url):
        platform_id = constants.codechef
        return True

    # regex matching for codeforces url
    regex_validator = re.compile(constants.codeforces_regex)
    if re.match(regex_validator, comp_url):
        platform_id = constants.codeforces
        return True

    return False


def perform_operations_on_url(comp_url):
    params = parse_url(comp_url)

    if len(params) < 1:
        printer.new_lines()
        print(
            rangebi.get_in_danger(
                "Error parsing the URL!"
            )
        )
        return False
    else:
        return prepare_battlezone(params, comp_url)


def parse_url(comp_url):
    problem_urls = []

    if platform_id == constants.codechef:
        problem_urls = codechef.get_codechef_problem_urls(comp_url)
    elif platform_id == constants.codeforces:
        problem_urls = codeforces.get_codeforces_problem_urls(comp_url)

    return problem_urls


def prepare_battlezone(problem_urls, comp_url):
    if not move_pointer():
        return False

    result = False

    if platform_id == constants.codechef:
        result = codechef.prepare_for_codechef_battle(problem_urls, comp_url)
    elif platform_id == constants.codeforces:
        result = codeforces.prepare_for_codeforces_battle(problem_urls, comp_url)

    return result


def move_pointer():
    try:
        if (not (os.getenv(constants.is_setup_done) is None)) and (int(os.getenv(constants.is_setup_done)) == 1):
            if not (os.getenv(constants.project_path) is None):
                os.chdir(os.getenv(constants.project_path))
                logger.info("Changing directory to: " + os.getenv(constants.project_path))
            else:
                os.makedirs(constants.startcp_default_folder, exist_ok=True)
                os.chdir(constants.startcp_default_folder)
                logger.info("Making if not exists and changing directory to: " + constants.startcp_default_folder)
        else:
            # lets go home by default
            os.makedirs(constants.startcp_default_folder, exist_ok=True)
            os.chdir(constants.startcp_default_folder)
            logger.info("Making if not exists and changing directory to: " + constants.startcp_default_folder)
        return True
    except Exception:
        return False
