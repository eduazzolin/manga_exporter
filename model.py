import os

from PIL import Image
from PyPDF2 import PdfReader, PdfWriter #TODO add to requirements.txt


class Series:
    def __init__(self, name: str, author: str, root: str, cover_size: list = None, dictionary: list = None,
                 volumes: list = [],
                 volumes_filename_template: str = None) -> object:
        """
        Initialize a Series object.

        :param name: The name of the series.
        :param author: The author of the series.
        :param root: The root folder where the series is located.
        :param cover_size: The size of the cover.
        :param dictionary: A list of dictionaries with volume, start and end.
        :param volumes: A list of Volume objects.
        :param volumes_filename_template: The template for the filename of the volumes.
        """
        self.name = name
        self.author = author
        self.root = root
        self.cover_size = cover_size
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
                          float(dictionary_entry['first_chapter']) <= chapter.number <= float(
                              dictionary_entry['last_chapter'])]
            )
            self.volumes.append(volume)

    def get_all_chapters(self) -> list:
        """
        Iterates over the root folder and returns a list of Chapter objects based
        on the PDF files found.

        :return: list of Chapter objects sorted by chapter number.
        """
        chapter_folders = [folder for folder in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, folder))
                           if folder.startswith('Chapter')]
        pdf_files = [pdf for pdf in os.listdir(self.root) if pdf.endswith('.pdf') if pdf.startswith('Chapter')]
        chapters = []
        for folder in chapter_folders:
            chapter = Chapter()
            chapter.series = self
            chapter.filename = folder + '.pdf' if folder + '.pdf' in pdf_files else None
            chapter.number = float(folder[folder.find(' ') + 1:folder.find('-') - 1])
            chapter.path = os.path.join(self.root, chapter.filename) if chapter.filename is not None else None
            chapter.folder_path = os.path.join(self.root, folder)
            chapters.append(chapter)
        return sorted(chapters, key=lambda x: x.number)

    def export_chapters(self):
        """
        Export chapters of the series by converting images to PDF.
        """

        folders = [folder for folder in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, folder))]
        folders = sorted(folders, key=lambda x: float(x[x.find(' ') + 1:x.find('-') - 1]))
        for folder in folders:
            try:
                images_path = [os.path.join(self.root, folder, image) for image in
                               os.listdir(os.path.join(self.root, folder))]
                images_img = [Image.open(image_path) for image_path in images_path]
                images_rgb = [img.convert('RGB') for img in images_img]
                images_rgb.pop(0).save(f'{os.path.join(self.root, folder)}.pdf', save_all=True,
                                       append_images=images_rgb)
                size = os.path.getsize(f'{os.path.join(self.root, folder)}.pdf')
                print(f'{folder}.pdf {Colors.GREEN}created! {size / 1000000:.2f} MB{Colors.ENDC}')
            except Exception as e:
                print(f'{folder}.pdf {Colors.RED}ERROR: {e}{Colors.ENDC}')
                continue

    def resize_volume_covers(self):
        """
        It will iterate over the first chapter of each volume and resize the cover to the specified size.
        Creating a new file called 00.jpg in the folder of the first chapter.
        """
        all_chapters = self.get_all_chapters()
        first_chapter_numbers = [d['first_chapter'] for d in self.dictionary]
        all_first_chapters = [chapter for chapter in all_chapters if chapter.number in first_chapter_numbers]
        for c in all_first_chapters:
            try:
                c.resize_cover_to_(self.cover_size[0], self.cover_size[1])
                print(f'{c.folder_path}/00.jpg {Colors.GREEN}created!{Colors.ENDC}')
            except Exception as e:
                print(f'{c.folder_path}/00.jpg {Colors.RED}ERROR: {e}{Colors.ENDC}')
                continue

    def export_volumes(self):
        """
        Export volumes of the series by merging the chapters into a single PDF.
        """
        for volume in self.volumes:
            try:
                if len(volume.chapters) == 0:
                    raise Exception(f"{Colors.RED}No chapter found!{Colors.ENDC}")
                merger = PdfWriter()
                for chapter in volume.chapters:
                    if chapter.path is not None:
                        merger.append(chapter.path)
                    else:
                        raise Exception(f"Missing chapter's PDF file")
                merger.write(volume.path)
                size = os.path.getsize(volume.path)
                if size / 100000 > 1:
                    print(f'{volume.filename} {Colors.GREEN}created! {size / 1000000:.2f} MB {Colors.ENDC}')
                else:
                    raise Exception(f"{Colors.RED}Something went wrong!{Colors.ENDC}")
                merger.close()
            except Exception as e:
                print(f'{volume.filename} {Colors.RED}ERROR: {e}{Colors.ENDC}')

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
    def __init__(self, number: float = None, filename: str = None, folder_path: str = None, path: str = None):
        """
        Initialize a Chapter object.

        :param number: The number of the chapter.
        :param filename: The filename of the chapter in PDF.
        :param folder_path: The path of the folder containing the chapter's images.
        :param path: The path of the chapter in PDF.
        """
        self.number = number
        self.filename = filename
        self.path = path
        self.folder_path = folder_path

    def resize_cover_to_(self, height: int, width: int):
        """
        Resize the cover of the chapter to the specified height and width. First the image is resized to the
        specified width and then cropped to the specified height by the center.
        :param height: the height of the cover
        :param width:  the width of the cover
        """
        # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
        # https://stackoverflow.com/questions/20361444/cropping-an-image-with-python-pillow

        image = Image.open(self.folder_path + '/01.jpg')
        w_percent = (width / float(image.size[0]))
        height_before_crop = int((float(image.size[1]) * float(w_percent)))
        c_left = 0
        c_right = width
        c_top = (height_before_crop - height) / 2
        c_bottom = ((height_before_crop - height) / 2) + height
        result = ((image.resize((width, height_before_crop), Image.Resampling.LANCZOS)
                   .crop((int(c_left), int(c_top), int(c_right), int(c_bottom))))
                  .save(os.path.join(self.folder_path, '00.jpg')))

    def resize_cover_to_with_white_lateral_borders(self, height: int, width: int):
        """
        Resize the cover of the chapter to the specified height and width. First the image is resized to the
        specified height and then is pasted in a white background with the specified width and height.
        :param height: the height of the cover
        :param width:  the width of the cover
        """
        # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
        # https://stackoverflow.com/questions/20361444/cropping-an-image-with-python-pillow

        image = Image.open(self.folder_path + '/01.jpg')
        h_percent = (height / float(image.size[1]))
        w_before_crop = int((float(image.size[0]) * float(h_percent)))

        w_difference = abs(width - w_before_crop) // 2
        new_image = Image.new("RGB", (width, height), (255, 255, 255))
        paste_position = (w_difference, 0)
        (image.resize((w_before_crop, height), Image.Resampling.LANCZOS)
         .save(os.path.join(self.folder_path, '00.jpg')))

        new_image.paste(Image.open(self.folder_path + '/00.jpg'), paste_position)
        new_image.save(os.path.join(self.folder_path, '00.jpg'))


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
