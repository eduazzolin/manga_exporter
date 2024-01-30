# Manga Exporter for Houdoku
## Description
This is a simple tool to export your manga library from [Houdoku](https://github.com/xgi/houdoku)
to PDF files. It is written in Python and uses [pypdf](https://pypdf.readthedocs.io/en/stable/) and [Pillow](https://pillow.readthedocs.io/en/stable/) to generate the PDFs.
I've made this tool because I wanted to export my manga library to PDFs so I can read them on my **Kindle**.
### 1. Export each chapter to a separate PDF file.
This function will export each chapter in your library to a separate PDF file. It will iterate through all the chapters folders and group the images into PDF files.
### 2. Group chapters into volumes and export each volume to a separate PDF file.
Based on a manually created dictionary, this function will group the chapters into volumes and export each volume to a separate PDF file. 
💡 _Tip: You can later use [Calibre](https://calibre-ebook.com/) to convert the PDF files to a Kindle supported format with covers and metadata._
## How to use
### 1. Download this repository and install the requirements.
First you need to make sure that you have Python installed, then you can download this repository and install the required packages using pip:
```bash
git clone https://github.com/eduazzolin/manga_exporter.git
cd manga_exporter
pip install -r requirements.txt
```
### 2. Edit the `config.json` file.
For the script to work, you need to edit the `config.json` file. The file contains the following fields:
- `NAME`: The name of the series. e.g. 'Berserk'
- `AUTHOR`: The author of the series. e.g. 'Kentaro Miura'
- `ROOT`: The root folder of the series. e.g. 'C:\\Users\\eduaz\\mangas\\Berserk'
- `VOLUME_FILENAME_TEMPLATE`: The template for the volume filename. You can use `[NAME]`, `[AUTHOR]` AND `[VOLUME]` as placeholders e.g. `[NAME] Vol. [VOLUME].pdf` -> 'Berserk Vol. 18.pdf'
- `DICTIONARY`: A list of dictionaries containing the volume number and the first and last chapter of the volume. e.g. `[{"volume": 1, "first_chapter": 1, "last_chapter": 5}, {"volume": 2, "first_chapter": 6, "last_chapter": 10}]` ?? tip: you can copy and paste the wikipedia page of the series into an IA to generate the dictionary according to the dictionary rules.
#### Example
```json
{
  "NAME": "Berserk",
  "AUTHOR": "Kentaro Miura",
  "ROOT": "C:\\Users\\eduaz\\mangas\\Berserk",
  "VOLUME_FILENAME_TEMPLATE": "[NAME] Vol. [VOLUME].pdf",
  "DICTIONARY": [
    { "volume": 1, "first_chapter": 0.01, "last_chapter": 0.03 },
    { "volume": 2, "first_chapter": 0.04, "last_chapter": 0.05 },
    { "volume": 3, "first_chapter": 0.06, "last_chapter": 0.09 },
    { "volume": 4, "first_chapter": 0.1, "last_chapter": 0.14 },
    { "volume": 5, "first_chapter": 0.15, "last_chapter": 6 },
    { "volume": 6, "first_chapter": 7, "last_chapter": 16 },
    { "volume": 7, "first_chapter": 17, "last_chapter": 26 },
    { "volume": 8, "first_chapter": 27, "last_chapter": 36 },
    { "volume": 9, "first_chapter": 37, "last_chapter": 47 },
    { "volume": 10, "first_chapter": 48, "last_chapter": 58 },
    { "volume": 11, "first_chapter": 59, "last_chapter": 68 },
    { "volume": 12, "first_chapter": 69, "last_chapter": 78 },
    { "volume": 13, "first_chapter": 80, "last_chapter": 91 },
    { "volume": 14, "first_chapter": 92, "last_chapter": 98 },
    { "volume": 15, "first_chapter": 100, "last_chapter": 109 },
    { "volume": 16, "first_chapter": 111, "last_chapter": 120 },
    { "volume": 17, "first_chapter": 122, "last_chapter": 132 },
    { "volume": 18, "first_chapter": 133, "last_chapter": 143 },
    { "volume": 19, "first_chapter": 144, "last_chapter": 154 },
    { "volume": 20, "first_chapter": 155, "last_chapter": 165 },
    { "volume": 21, "first_chapter": 166, "last_chapter": 176 },
    { "volume": 22, "first_chapter": 177, "last_chapter": 186 },
    { "volume": 23, "first_chapter": 187, "last_chapter": 196 },
    { "volume": 24, "first_chapter": 197, "last_chapter": 206 },
    { "volume": 25, "first_chapter": 207, "last_chapter": 216 },
    { "volume": 26, "first_chapter": 217, "last_chapter": 226 },
    { "volume": 27, "first_chapter": 227, "last_chapter": 236 },
    { "volume": 28, "first_chapter": 237, "last_chapter": 246 },
    { "volume": 29, "first_chapter": 247, "last_chapter": 256 },
    { "volume": 30, "first_chapter": 257, "last_chapter": 266 },
    { "volume": 31, "first_chapter": 267, "last_chapter": 276 },
    { "volume": 32, "first_chapter": 277, "last_chapter": 286 },
    { "volume": 33, "first_chapter": 287, "last_chapter": 296 },
    { "volume": 34, "first_chapter": 297, "last_chapter": 306 },
    { "volume": 35, "first_chapter": 307, "last_chapter": 315 },
    { "volume": 36, "first_chapter": 316, "last_chapter": 324 },
    { "volume": 37, "first_chapter": 325, "last_chapter": 333 },
    { "volume": 38, "first_chapter": 334, "last_chapter": 342 },
    { "volume": 39, "first_chapter": 343, "last_chapter": 350 },
    { "volume": 40, "first_chapter": 351, "last_chapter": 357 },
    { "volume": 41, "first_chapter": 358, "last_chapter": 364 }
  ]
}
```
### 3. Run the script.
To run the script, you need to run the following command:
```bash
python manga-exporter.py
```
