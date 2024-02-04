import json
from model import *


class Main:

    @staticmethod
    def print_logo():
        """
        Prints the logo of the program.
        """
        print(f"""
    ┳┳┓┏┓┳┓┏┓┏┓  ┏┓┏┓┏┓┏┓┏┓┳┓┏┳┓┏┓┳┓
    ┃┃┃┣┫┃┃┃┓┣┫  ┣  ┃┃ ┃┃┃┃┣┫ ┃ ┣ ┣┫
    ┛ ┗┛┗┛┗┗┛┛┗  ┗┛┗┛┗┛┣┛┗┛┛┗ ┻ ┗┛┛┗
                         {Colors.GRAY}for Houdoku{Colors.ENDC}
    """)

    @staticmethod
    def show_menu(series):
        """
        Shows the main menu and calls the appropriate method based on the user's choice.
        :param series: the Series object
        """
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

    @staticmethod
    def select_dictionary() -> object:
        """
        Selects a dictionary from the dictionaries folder.
        :return: json object
        """
        dictionary_list = [f for f in os.listdir('dictionaries') if f.endswith('.json')]

        print(f"{Colors.BOLD}Select a dictionary:{Colors.ENDC}")
        for i, dictionary in enumerate(dictionary_list):
            print(f"{i + 1} - {dictionary}")
        choice = input('\nType the number of the dictionary and press Enter: ')
        with open(f'dictionaries\\{dictionary_list[int(choice) - 1]}', 'r') as config_file:
            return json.load(config_file)

    @staticmethod
    def show_config(config):
        """
        Shows the configuration of the series.
        :param config: json object
        """
        print(f"""
    {Colors.BOLD}CONFIGURATION{Colors.ENDC}
    {Colors.BOLD}Name:{Colors.ENDC} {config["NAME"]}
    {Colors.BOLD}Author:{Colors.ENDC} {config["AUTHOR"]}
    {Colors.BOLD}Root folder:{Colors.ENDC} {config["ROOT"]}
    {Colors.BOLD}Volume filename template:{Colors.ENDC} {config["VOLUME_FILENAME_TEMPLATE"]}
    {Colors.BOLD}Cover size:{Colors.ENDC} {config["COVER_SIZE"]}
    {Colors.BOLD}Dictionary:{Colors.ENDC} {"Ok!" if config["DICTIONARY"] else "Not Ok!"}
    """)


if __name__ == '__main__':
    Main.print_logo()
    config = Main.select_dictionary()
    Main.show_config(config)
    series: Series = Series(
        name=config["NAME"],
        author=config["AUTHOR"],
        root=config["ROOT"],
        volumes_filename_template=config["VOLUME_FILENAME_TEMPLATE"],
        cover_size=config["COVER_SIZE"],
        dictionary=config["DICTIONARY"],
    )
    Main.show_menu(series)
