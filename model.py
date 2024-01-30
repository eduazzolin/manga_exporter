import os

from PIL import Image
from pypdf import PdfWriter


class Series:
    def __init__(self, name: str, author: str, root: str, dictionary: list = None, volumes: list = [],
                 volumes_filename_template: str = None) -> object:
        """
        Initialize a Series object.

        :param name: The name of the series.
        :param author: The author of the series.
        :param root: The root folder where the series is located.
        :param dictionary: A list of dictionaries with volume, start and end.
        :param volumes: A list of Volume objects.
        :param volumes_filename_template: The template for the filename of the volumes.
        """
        self.name = name
        self.author = author
        self.root = root
        self.dictionary = sorted(dictionary, key=lambda x: x['volume'])
        self.volumes = volumes
        self.volumes_filename_template = volumes_filename_template

    def generate_volumes(self):
        """
        Generates a list of Volume objects based on the dictionary.
        """
        all_chapters = self.get_all_chapters()
        for dictionary_entry in self.dictionary:
            volume = Volume(
                number=float(dictionary_entry['volume']),
                series=self,
                chapters=[chapter for chapter in all_chapters if
                          float(dictionary_entry['first_chapter']) <= chapter.number <= float(dictionary_entry['last_chapter'])]
            )
            self.volumes.append(volume)

    def get_all_chapters(self) -> list:
        """
        Iterates over the root folder and returns a list of Chapter objects based
        on the PDF files found.

        :return: list of Chapter objects sorted by chapter number.
        """
        pdf_files = [pdf for pdf in os.listdir(self.root) if pdf.endswith('.pdf') if pdf.startswith('Chapter')]
        chapters = []
        for pdf in pdf_files:
            chapter = Chapter()
            chapter.series = self
            chapter.filename = pdf
            chapter.number = float(pdf[pdf.find(' ') + 1:pdf.find('-') - 1])
            chapter.path = os.path.join(self.root, pdf)
            chapters.append(chapter)
        return sorted(chapters, key=lambda x: x.number)

    def export_chapters(self):
        """
        Export chapters of the series by converting images to PDF.
        """

        folders = [folder for folder in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, folder))]
        for folder in folders:
            try:
                images_path = [os.path.join(self.root, folder, image) for image in
                               os.listdir(os.path.join(self.root, folder))]
                images_img = [Image.open(image_path) for image_path in images_path]
                images_rgb = [img.convert('RGB') for img in images_img]
                images_rgb.pop(0).save(f'{os.path.join(self.root, folder)}.pdf', save_all=True,
                                       append_images=images_rgb)

                print(f'{folder}.pdf {Colors.GREEN}created!{Colors.ENDC}')
            except Exception as e:
                print(e)
                continue

    def export_volumes(self):
        """
        Export volumes of the series by merging the chapters into a single PDF.
        """
        for volume in self.volumes:
            if len(volume.chapters) == 0:
                print(f'{volume.filename} {Colors.RED}ERROR: No chapter found!{Colors.ENDC}')
                continue
            merger = PdfWriter()
            for chapter in volume.chapters:
                merger.append(chapter.path)
            merger.write(volume.path)
            size = os.path.getsize(volume.path)
            if size / 100000 > 1:
                print(f'{volume.filename} {Colors.YELLOW}created! {size / 1000000} MB {Colors.ENDC}')
            else:
                print(f'{volume.filename} {Colors.RED}ERROR: Something went wrong!{Colors.ENDC}')
            merger.close()


class Volume:
    """
    Initialize a Volume object.

    :param number: The number of the volume.
    :param series: The Series object the volume belongs to.
    :param chapters: A list of Chapter objects.
    """

    def __init__(self, number: float, series: Series, chapters: list = None):
        self.number = number
        self.chapters = chapters
        self.filename = self.generate_filename(series)
        self.path = os.path.join(series.root, self.filename)

    def generate_filename(self, series: Series) -> str:
        """
        Generate the filename for the volume based on the series' filename template.

        :param series: The Series object the volume belongs to.
        """
        filename_temp = series.volumes_filename_template
        filename_temp = filename_temp.replace('[AUTHOR]', series.author)
        filename_temp = filename_temp.replace('[NAME]', series.name)
        filename_temp = filename_temp.replace('[VOLUME]', f'{self.number:g}')
        return filename_temp


class Chapter:
    def __init__(self, number: float = None, filename: str = None, path: str = None):
        """
        Initialize a Chapter object.

        :param number: The number of the chapter.
        :param filename: The filename of the chapter.
        :param path: The path of the chapter.
        """
        self.number = number
        self.filename = filename
        self.path = path


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

    @staticmethod
    def job_done():
        """
        Print a completion message.
        """
        print(f"""{Colors.BLUE}

                        job done!        
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠞⢳⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡔⠋⠀⢰⠎⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢆⣤⡞⠃⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢠⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⣀⣾⢳⠀⠀⠀⠀⢸⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⣀⡤⠴⠊⠉⠀⠀⠈⠳⡀⠀⠀⠘⢎⠢⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀
        ⠳⣄⠀⠀⡠⡤⡀⠀⠘⣇⡀⠀⠀⠀⠉⠓⠒⠺⠭⢵⣦⡀⠀⠀⠀
        ⠀⢹⡆⠀⢷⡇⠁⠀⠀⣸⠇⠀⠀⠀⠀⠀⢠⢤⠀⠀⠘⢷⣆⡀⠀
        ⠀⠀⠘⠒⢤⡄⠖⢾⣭⣤⣄⠀⡔⢢⠀⡀⠎⣸⠀⠀⠀⠀⠹⣿⡀
        ⠀⠀⢀⡤⠜⠃⠀⠀⠘⠛⣿⢸⠀⡼⢠⠃⣤⡟⠀⠀⠀⠀⠀⣿⡇
        ⠀⠀⠸⠶⠖⢏⠀⠀⢀⡤⠤⠇⣴⠏⡾⢱⡏⠁⠀⠀⠀⠀⢠⣿⠃
        ⠀⠀⠀⠀⠀⠈⣇⡀⠿⠀⠀⠀⡽⣰⢶⡼⠇⠀⠀⠀⠀⣠⣿⠟⠀
        ⠀⠀⠀⠀⠀⠀⠈⠳⢤⣀⡶⠤⣷⣅⡀⠀⠀⠀⣀⡠⢔⠕⠁⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠫⠿⠿⠿⠛⠋⠁⠀⠀⠀⠀
                {Colors.ENDC}""")
