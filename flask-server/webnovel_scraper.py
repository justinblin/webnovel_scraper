import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re

def read_chapter(chapter_link: str, series_title: str = "") -> None:
    """
    Open and read a chapter then stores it in a file
    """

    # check link compatibility
    if re.search("^https://.*royalroad.com/fiction/.*/chapter/", chapter_link) == None:
        raise Exception("Provided link <" + chapter_link + "> isn't a chapter link from royal road")

    # pull chapter title and content
    chapter_html = requests.get(chapter_link).content
    chapter_soup = BeautifulSoup(chapter_html, 'html.parser')

    chapter_title_text = chapter_soup.find("title").get_text()
    chapter_title_text = chapter_title_text[:chapter_title_text.find("|")].strip()
    chapter_content_text = chapter_soup.find("div", class_ = "chapter-content").get_text().strip()

    # build folder name if using series_title
    folder_name = ""
    if series_title != "":
        folder_name += "../" + series_title + "/"
        Path(folder_name).mkdir(parents=True, exist_ok=True)

    # write out chapter content
    file_handler = open(folder_name + chapter_title_text + ".txt", "w")
    file_handler.write(chapter_content_text)
    file_handler.close()


def find_chapter_index_by_name(chapter_html_list, chapter_name: str) -> int:
    """
    Find chapter index using chapter name
    """

    for current_chapter_index, current_chapter_html in enumerate(chapter_html_list):
        if current_chapter_html.find("a").string.strip() == chapter_name:
            return current_chapter_index
    raise Exception("Chapter name \"" + chapter_name + "\" not found")

def read_series(series_link: str, chapter_start_input: int | str = 0, chapter_end_input: int | str = None) -> None:
    """
    Read the chapters of a series and store them into files based on chapter index or name. 
    For search by index, chapter_start_input is inclusive, chapter_end_input is exclusive.
    For search by name, all inputs are inclusive
    """

    # check link compatibility
    if re.search("^https://.*royalroad.com/fiction/.*/chapter/", series_link) != None or\
        re.search("^https://.*royalroad.com/fiction/",series_link) == None:
        raise Exception("Provided link <" + series_link + "> isn't a series link from Royal Road")

    # pull series title and chapters
    series_html = requests.get(series_link).content
    series_soup = BeautifulSoup(series_html, 'html.parser')

    series_title_text = series_soup.find("title").get_text()
    series_title_text = series_title_text[:series_title_text.find("|")].strip()

    chapter_html_list = series_soup.find_all("tr", class_ = "chapter-row")

    # search by name/get default indices
    if type(chapter_start_input) == str:
        chapter_start_input: int = find_chapter_index_by_name(chapter_html_list, chapter_start_input)
    if type(chapter_end_input) == str:
        chapter_end_input: int = find_chapter_index_by_name(chapter_html_list, chapter_end_input) + 1
    elif type(chapter_end_input) == None:
        chapter_end_input: int = len(chapter_html_list)

    # go through the links and read each chapter
    for current_chapter_index in range(chapter_start_input, chapter_end_input):
        current_chapter_html = chapter_html_list[current_chapter_index]
        read_chapter("https://royalroad.com" + current_chapter_html.find("a")["href"], series_title_text)


# read_chapter("https://www.royalroad.com/fiction/64916/hell-difficulty-tutorial/chapter/1121432/chapter-1", "Hell Difficulty Tutorial")
read_series("https://www.royalroad.com/fiction/64916/hell-difficulty-tutorial/", "Chapter 1", "Side story (non-canon) - A Nibble to Remember")