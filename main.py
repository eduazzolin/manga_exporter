import json
import os

from model import *


def print_logo():
    print(f"""
┳┳┓┏┓┳┓┏┓┏┓  ┏┓┏┓┏┓┏┓┏┓┳┓┏┳┓┏┓┳┓
┃┃┃┣┫┃┃┃┓┣┫  ┣  ┃┃ ┃┃┃┃┣┫ ┃ ┣ ┣┫
┛ ┗┛┗┛┗┗┛┛┗  ┗┛┗┛┗┛┣┛┗┛┛┗ ┻ ┗┛┛┗
                     {Colors.GRAY}for Houdoku{Colors.ENDC}
""")


def show_menu(series):
    choice = ''
    while choice != '0':
        print(f"""    
Options:

{Colors.BOLD}1 - RESIZE THE COVERS{Colors.ENDC}
    {Colors.GRAY}resizes the covers of each volume to the specified
    size{Colors.ENDC}

{Colors.BOLD}2 - EXPORT CHAPTERS TO PDF{Colors.ENDC}
    {Colors.GRAY}collects  all  images from each chapter folder and
    exports them to separate pdf files{Colors.ENDC}

{Colors.BOLD}3 - EXPORT VOLUMES TO PDF{Colors.ENDC}
    {Colors.GRAY}collects  all chapters from  each volume based on
    the dictionary  and exports them to separate  pdf 
    files{Colors.ENDC}
    
{Colors.BOLD}4 - EXPORT EVERYTHING{Colors.ENDC}
    {Colors.GRAY}does both of the above: exports  the chapters then 
    the volumes{Colors.ENDC}
""")
        choice = input("\n-> ")
        if choice == '1':
            series.resize_volume_covers()
            Colors.job_done()
        if choice == '2':
            series.export_chapters()
            Colors.job_done()
        if choice == '3':
            series.generate_volumes()
            series.export_volumes()
            Colors.job_done()
        if choice == '4':
            series.export_chapters()
            series.generate_volumes()
            series.export_volumes()
            Colors.job_done()
            choice = '0'


def select_dictionary() -> object:
    dictionary_list = [f for f in os.listdir('dictionaries') if f.endswith('.json')]

    print(f"{Colors.BOLD}Select a dictionary:{Colors.ENDC}")
    for i, dictionary in enumerate(dictionary_list):
        print(f"{i + 1} - {dictionary}")
    choice = input('\nType the number of the dictionary and press Enter: ')
    with open(f'dictionaries\\{dictionary_list[int(choice) - 1]}', 'r') as config_file:
        return json.load(config_file)


def show_config(config):
    print(f"""
{Colors.BOLD}CONFIGURATION{Colors.ENDC}
{Colors.BOLD}Name:{Colors.ENDC} {config["NAME"]}
{Colors.BOLD}Author:{Colors.ENDC} {config["AUTHOR"]}
{Colors.BOLD}Root folder:{Colors.ENDC} {config["ROOT"]}
{Colors.BOLD}Volume filename template:{Colors.ENDC} {config["VOLUME_FILENAME_TEMPLATE"]}
{Colors.BOLD}Cover size:{Colors.ENDC} {config["COVER_SIZE"]}
{Colors.BOLD}Dictionary:{Colors.ENDC} {"Ok!" if config["DICTIONARY"] else "Not Ok!"}
""")


class Main:
    print_logo()
    config = select_dictionary()

    NAME = config["NAME"]
    AUTHOR = config["AUTHOR"]
    ROOT = config["ROOT"]
    VOLUME_FILENAME_TEMPLATE = config["VOLUME_FILENAME_TEMPLATE"]
    COVER_SIZE = config["COVER_SIZE"]
    DICTIONARY = config["DICTIONARY"]

    show_config(config)
    series: Series = Series(
        name=NAME,
        author=AUTHOR,
        root=ROOT,
        volumes_filename_template=VOLUME_FILENAME_TEMPLATE,
        cover_size=COVER_SIZE,
        dictionary=DICTIONARY,
    )

    show_menu(series)
