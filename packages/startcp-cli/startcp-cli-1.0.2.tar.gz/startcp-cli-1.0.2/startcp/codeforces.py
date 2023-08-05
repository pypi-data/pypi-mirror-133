import os
from pathlib import Path
import shutil
import re
import requests

from bs4 import BeautifulSoup

try:
    import printer, constants
except Exception:
    from startcp import printer, constants


rangebi = printer.Rangebi()


def get_codeforces_problem_urls(comp_url):
    problem_urls = []

    problem_site = requests.get(comp_url)

    if (problem_site.status_code == 200):
        problems_soup = BeautifulSoup(problem_site.content, 'html.parser')
        problems_table = problems_soup.find_all("table", {"class": "problems"})

        if len(problems_table) == 1:
            problem_count = len(problems_table[0].find_all("tr")) - 1
            for p_i in range(problem_count):
                problem_url = comp_url + '/problem/' + chr(65 + p_i)
                problem_urls.append(problem_url)

    return problem_urls


def prepare_for_codeforces_battle(problem_urls, comp_url):

    if (not (os.getenv(constants.is_setup_done) is None)) and (int(os.getenv(constants.is_setup_done)) == 1):
        if (not (os.getenv(constants.codeforces_folder_name) is None)) and (len(os.getenv(constants.codeforces_folder_name)) > 0):
            os.makedirs(os.getenv(constants.codeforces_folder_name), exist_ok=True)
            os.chdir(os.getenv(constants.codeforces_folder_name))
        else:
            os.makedirs(constants.codeforces, exist_ok=True)
            os.chdir(constants.codeforces)

    codeforces_comp_id = comp_url.split("/")[-1]

    os.makedirs(codeforces_comp_id, exist_ok=True)
    os.chdir(codeforces_comp_id)


    for problem_url in problem_urls:
        problem_folder_name = problem_url.split("/")[-1]
        os.makedirs(problem_folder_name, exist_ok=True)

        problem_response = requests.get(problem_url)

        if (problem_response.status_code == 200):

            if not os.path.isfile(problem_folder_name + "/" + "problem.html"):
                html_str = get_java_script_code_for_problem(problem_url)

                problem_html_file = problem_folder_name + "/" + "problem.html"

                with open(problem_html_file, "w+") as outfile:
                    outfile.write(html_str)

            tmplt_file_created = True
            if (not (os.getenv(constants.use_template) is None)) and (int(os.getenv(constants.use_template)) == 1):
                try:
                    if not (os.getenv(constants.main_lang_template_path) is None):
                        if Path(os.getenv(constants.main_lang_template_path)).is_file():
                            shutil.copy(os.getenv(constants.main_lang_template_path), problem_folder_name + "/")
                            if not (os.getenv(constants.backup_lang_template_path) is None):
                                if Path(os.getenv(constants.backup_lang_template_path)).is_file():
                                    shutil.copy(os.getenv(constants.backup_lang_template_path), problem_folder_name + "/")
                        else:
                            tmplt_file_created = False
                    else:
                        tmplt_file_created = False
                except Exception:
                    tmplt_file_created = False
            else:
                tmplt_file_created = False

            if not tmplt_file_created:
                if not os.path.isfile(problem_folder_name + "/" + "sol.py"):
                    Path(problem_folder_name + "/" + "sol.py").touch()

                if not os.path.isfile(problem_folder_name + "/" + "sol.cpp"):
                    Path(problem_folder_name + "/" + "sol.cpp").touch()

            try:
                problems_soup = BeautifulSoup(problem_response.content, 'html.parser')

                id = 1
                input_str = problems_soup.find_all("div", {"class": "input"})[0].find_all("pre")[0].text
                output_str = problems_soup.find_all("div", {"class": "output"})[0].find_all("pre")[0].text

                input_filename = problem_folder_name + "/" + "in" + str(id) + ".txt"
                output_filename = problem_folder_name + "/" + "out" + str(id) + ".txt"

                with open(input_filename, "w+") as outfile:
                    outfile.write(input_str)

                with open(output_filename, "w+") as outfile:
                    outfile.write(output_str)

            except Exception as e:
                print(e)
                continue

def get_java_script_code_for_problem(problem_url):
    return """
    <html>
        <body>
            <script>
                window.location.replace('{problem_url}');
            </script>
        </body>
    </html>
    """.format(problem_url=problem_url)