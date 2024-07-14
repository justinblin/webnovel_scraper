import requests
from bs4 import BeautifulSoup
from pathlib import Path


def read_chapter(chapter_link: str, series_title: str = "") -> None:
    """
    Open and read a chapter then stores it in a file
    """

    chapter_html = requests.get(chapter_link).content
    chapter_soup = BeautifulSoup(chapter_html, 'html.parser')

    chapter_title_text = chapter_soup.find("title").get_text()
    chapter_title_text = chapter_title_text[:chapter_title_text.find("|")].strip()
    chapter_content_text = chapter_soup.find("div", class_ = "chapter-content").get_text().strip()

    folder_name = ""
    if series_title != "":
        folder_name += series_title + "/"
        Path(folder_name).mkdir(parents=True, exist_ok=True)

    file_handler = open(folder_name + chapter_title_text + ".txt", "w")
    file_handler.write(chapter_content_text)
    file_handler.close()


def read_series(series_link: str, chapter_start_index: int = 0, chapter_end_index: int = None) -> None:
    """
    Read the chapters of a series and store them into files. Parameter chapter_start_index is inclusive, chapter_end_index is exclusive
    """

    series_html = requests.get(series_link).content
    series_soup = BeautifulSoup(series_html, 'html.parser')

    series_title_text = series_soup.find("title").get_text()
    series_title_text = series_title_text[:series_title_text.find("|")].strip()

    chapter_html_list = series_soup.find_all("tr", class_ = "chapter-row")

    if type (chapter_end_index) == None:
        chapter_end_index = len(chapter_html_list)

    for current_chapter_index in range(chapter_start_index, chapter_end_index):
        current_chapter_html = chapter_html_list[current_chapter_index]
        read_chapter("https://royalroad.com" + current_chapter_html.find("a")["href"], series_title_text)


# read_chapter("https://www.royalroad.com/fiction/64916/hell-difficulty-tutorial/chapter/1121432/chapter-1", "Hell Difficulty Tutorial")
read_series("https://www.royalroad.com/fiction/64916/hell-difficulty-tutorial", 0, 2)