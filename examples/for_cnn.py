import sys
sys.path.append('../')

from base64 import urlsafe_b64encode
from src.utility_functions import download_a_file, article_file_exists
from src.utility_functions import the_requester, json_output_generator, extract_file_extension

from bs4 import BeautifulSoup
from re import sub as regreplace
import threading


class CNNSite:
    def __init__(self, the_url):
        self.the_url = the_url

    def read_content_information(self):
        the_rquester_response = the_requester(the_url=self.the_url)
        try:
            if the_rquester_response.get("url_response").status_code // 100 == 2:
                return {
                    "content": the_rquester_response.get("url_response").content,
                    "last_modified": the_rquester_response.get("url_response").headers.get("X-Last-Modified"),
                }
            else:
                return False
        except AttributeError:
            return False

    def parse_data(self, content_information=None):
        to_return = {}
        if not content_information:
            content_information = self.read_content_information()
        content = content_information.get("content")
        if content:
            to_return.update(content_information)
            soup = BeautifulSoup(content, "lxml")

            url = soup.find("meta", property="og:url").get("content")
            unique_id = urlsafe_b64encode(url.encode("utf8")).decode("utf8")

            if article_file_exists(unique_id=unique_id):
                return False

            to_return["url"] = url
            to_return["unique_id"] = unique_id

            article_section = soup.find("div", class_="article__content")
            if soup.title.contents:
                to_return["title"] = soup.title.contents[0]
            else:
                return False
            p_tags = article_section.find_all("p")
            list_of_p_tags_content = []
            if p_tags:
                for p in p_tags:
                    list_of_p_tags_content.append(p.contents[0])
            img_tags = article_section.find_all("img")
            list_of_img_tags_content = [
                {
                    "image_url": soup.find("meta", property="og:image").get("content"),
                    "image_name_on_save": f'{to_return.get("unique_id")}.{extract_file_extension(soup.find("meta", property="og:image").get("content"))}'
                }
            ]
            print(list_of_img_tags_content)
            if img_tags:
                for indx, img in enumerate(img_tags):
                    image_url = img["src"]
                    image_extension = extract_file_extension(image_url)
                    image_name_on_save = f'{to_return.get("unique_id")}.{indx}.{image_extension}'
                    list_of_img_tags_content.append({
                        "image_url": image_url,
                        "image_name_on_save": image_name_on_save
                    })
            threads = []
            for _ in list_of_img_tags_content:
                thread = threading.Thread(target=download_a_file, args=(_.get("image_url"), _.get("image_name_on_save")))
                thread.start()
                threads.append(thread)

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

            to_return["images_on_article"] = [x for x in list_of_img_tags_content]

            formed_body = ' '.join(list_of_p_tags_content).replace('\n', '')
            to_return["body"] = regreplace(r'\s+', ' ', formed_body).strip()
            to_return.pop("content")
            return to_return
        return to_return

    def display(self, data):
        print(data)
        return True

    def write_content_to_json_file(self, json_data, the_file_name):
        if not json_data and the_file_name:
           json_data = self.parse_data()
           the_file_name = json_data.get("unique_id")
        return json_output_generator(json_data=json_data, the_file_name=the_file_name)

    def operate_cnn_content_collector(self):
        content_inforomation = self.read_content_information()
        parsed_data = self.parse_data(content_information=content_inforomation)
        if parsed_data:
            self.display(data=parsed_data)
            self.write_content_to_json_file(json_data=parsed_data, the_file_name=parsed_data.get("unique_id"))
        return True


if __name__ == "__main__":
    cnn_links = [
        "https://edition.cnn.com/travel/airbus-overhead-airspace-l-bins/index.html",
        "https://edition.cnn.com/2023/12/21/health/sleep-mental-health-wellness/index.html",
        "http://www.edition.cnn.com/2024/02/14/tech/billions-in-ai-patents-get-new-regulations/index.html",
        "https://edition.cnn.com/2024/02/14/tech/billions-in-ai-patents-get-new-regulations/index.html"
    ]
    for _ in cnn_links:
        CNNSite(the_url=_).operate_cnn_content_collector()
