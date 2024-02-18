import json
import logging
from pathlib import Path

import requests
from random import choice
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

from urllib.parse import urlparse


def user_agent_switcher():
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0 whid/dtw5 macaddress/f8b46a253d81",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Internet Explorer/77.0.85.118 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.5.70 Safari/629.20.14"
    ]
    return choice(ua_list)


def the_requester(the_url):
    to_return = {}
    headers = {'user-agent': user_agent_switcher()}
    url_response = requests.get(
        url=the_url, allow_redirects=True,
        timeout=1, headers=headers
    )
    if url_response.status_code // 100 == 2:
        to_return["url_response"] = url_response
        # if url_response.history:
        #     to_return["url"] = url_response.url
        #     to_return["unique_id"] = soup.find("meta", "og:url").get("content")
        # else:
        #     to_return["url"] = the_url
        #     to_return["unique_id"] = urlsafe_b64encode(the_url.encode("utf8")).decode("utf8")
    else:
        return False
    return to_return


def json_output_generator(json_data, the_file_name, output_location="output"):
    try:
        os.mkdir(output_location)
    except FileExistsError:
        pass

    file_path = f"{output_location}/{the_file_name}.json"

    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    return True


def download_a_file(the_url, destination_filename=None, output_location="output"):
    try:
        os.mkdir(output_location)
    except FileExistsError:
        pass

    if not destination_filename:
        destination_filename = urlparse(the_url).path.split('/')[-1]

    headers = {'user-agent': user_agent_switcher()}
    url_response = requests.get(
        url=the_url, allow_redirects=True,
        timeout=50, headers=headers
    )
    if url_response.status_code == 200:
        with open(f"{output_location}/{destination_filename}", 'wb') as f:
            f.write(url_response.content)
        return {
            "destination_filename": destination_filename
        }
    else:
        return False


def extract_file_extension(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Get the path component of the URL
    path = parsed_url.path
    # Split the path by '/' and get the last part
    filename = path.split('/')[-1]
    # Split the filename by '.' and get the last part
    extension = filename.split('.')[-1]
    return extension


def list_files_in_directory(directory):
    return [file.stem for file in Path(directory).iterdir() if file.is_file()]


def article_file_exists(unique_id, output_location="output"):
    try:
        os.mkdir(output_location)
    except FileExistsError:
        pass

    files = list_files_in_directory(output_location)

    if unique_id in files:
        return True
    return False
