import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

@app.route("/test", methods=['POST'])
def test(): # has to return a json
    data = request.get_json(force=True)
    return {"status": "hi"}


def read_chapter(chapter_link: str, pathway: str) -> None:
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
    chapter_title_text = "".join( x for x in chapter_title_text if (x.isalnum() or x in "._- ")) # getting rid of illegal characters in the title
    print(chapter_title_text)

    chapter_content_text = chapter_soup.find("div", class_ = "chapter-content").get_text().strip()
    print("got chapter content text")
    # print(chapter_content_text)

    # print(pathway + "/" + chapter_title_text + ".txt")

    # build folder and write out chapter content
    Path(pathway + "/").mkdir(parents = True, exist_ok = True)
    file_handler = open(pathway + "/" + chapter_title_text + ".txt", "w", encoding = "utf-8")
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


def read_series(series_link: str, pathway: str, chapter_start_input: int | str = 0, chapter_end_input: int | str = None) -> None:
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
    series_title_text = "".join( x for x in series_title_text if (x.isalnum() or x in "._- ")) # getting rid of illegal characters in the title
    print(series_title_text)

    chapter_html_list = series_soup.find_all("tr", class_ = "chapter-row")

    # search by name/get default indices
    if type(chapter_start_input) == str and chapter_start_input != "":
        chapter_start_input: int = find_chapter_index_by_name(chapter_html_list, chapter_start_input)
    elif chapter_start_input == "":
        chapter_start_input: int = 0

    if type(chapter_end_input) == str and chapter_end_input != "":
        chapter_end_input: int = find_chapter_index_by_name(chapter_html_list, chapter_end_input) + 1
    elif chapter_end_input == "" or chapter_end_input == None: # does this work in python?
        chapter_end_input: int = len(chapter_html_list)

    # go through the links and read each chapter
    for current_chapter_index in range(chapter_start_input, chapter_end_input):
        current_chapter_html = chapter_html_list[current_chapter_index]
        read_chapter("https://royalroad.com" + current_chapter_html.find("a")["href"], pathway + "/" + series_title_text)


@app.route("/read_link", methods=['POST']) # is there supposed to be a methods thing here too?, maybe if it's in the header when it's sent, it has to be here
def read_link(): 
    try:
        data = request.get_json(force=True)

        if (data["linkType"] == "chapter"):
            read_chapter(data["link"], data["pathway"])
            return jsonify({"status": "Read Chapter"}) # does jsonify only accept dictionaries? returns have to be jsons
        
        elif (data["linkType"] == "series"):
            read_series(data["link"], data["pathway"], data["chapterStart"], data["chapterEnd"])
            return jsonify({"status": "Read Series"})
        
        else:
            return jsonify({"status": "Link Type Incorrect"})
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug = True)
    #read_series("https://www.royalroad.com/fiction/75359/on-foreign-soils-we-die", "C:/Users/justi/Desktop/Justin Lin/Personal Projects/Webnovel Scraper/Chapters", "Chapter 17 - A Minute Respite")