import json
import requests
from bs4 import BeautifulSoup, ResultSet
from lxml import etree

from bili_proj.utils.logger import get_logger
from bili_proj.utils.downloads import download_resource
from bili_proj.resource import load_yaml, extract_base_url, ensure_download_directory, resource_path


LOGGER = get_logger("bilibilib_get_audio", resource_path("../log/thi_proj.log"))

config = load_yaml(resource_path("../resources/download_items_pandas.yml"))
download_item = config["download_items"][0]["download_item"]

referer = extract_base_url(download_item["get_title_list_url"])
LOGGER.info(f"referer: {referer}")
# fake request head
HEADERS = {
    "User-Agent": str(download_item["user_agent"]),
    # 防盗链子
    "Referer": referer,
    "Cookie": str(download_item["cookie"])
}

def extract_play_list(url: str):
    response = requests.get(url, headers=HEADERS)
    res_text = response.text
    soup = BeautifulSoup(res_text, "html.parser")
    # extract title
    divs = soup.find_all("div", class_="title-txt")

    lst_title = None
    if isinstance(divs, ResultSet):
        lst_title = [div.get_text() for div in divs]

    return lst_title

def main():
    """
    raw -> https://www.bilibili.com/video/BV1vE411d7ht/?spm_id_from=333.788.recommend_more_video.0&vd_source=f230a650621ce31e8709b0bd5a3826fb
    changed to -> https://www.bilibili.com/video/BV1vE411d7ht?spm_id_from=333.788.videopod.episodes&vd_source=f230a650621ce31e8709b0bd5a3826fb
    next -> https://www.bilibili.com/video/BV1vE411d7ht?spm_id_from=333.788.videopod.episodes&vd_source=f230a650621ce31e8709b0bd5a3826fb&p=2
    """

    get_title_list_url = download_item["get_title_list_url"]
    download_url = download_item["download_url"]

    LOGGER.info(f"HEADERS:{HEADERS}")
    lst_play = extract_play_list(get_title_list_url)
    for index, value in enumerate(lst_play, start=1):
        print(f"{index}: {value}")
        # resource_url = extract_resource_download_url(f"{download_url}{index}", value)
        # download_resource(resource_url["audio_url"], resource_url["audio_path"], HEADERS)


if __name__ == "__main__":
    main()
