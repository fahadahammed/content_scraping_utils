from src.utility_functions import download_a_file, json_output_generator
from pdfquery import PDFQuery
import PyPDF2


class PDFops:
    def __init__(self, the_url):
        self.the_url = the_url

    def download_pdf_file(self):
        file_name = download_a_file(the_url=self.the_url)
        if file_name:
            return file_name
        else:
            return False

    def parse_data_from_pdf(self, pdf_file_location):
        the_file = f'output/{pdf_file_location.get("destination_filename")}'
        with open(the_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # Extracting title (first line)
            title = reader.pages[0].extract_text().split('\n')[0].strip()

            # Extracting body (remaining text)
            body = ''
            for page_num in range(1, len(reader.pages)):
                body += reader.pages[page_num].extract_text()

            return {
                "title": title,
                "body": body
            }

    def display(self, data):
        print(data)
        return True

    def write_content_to_json_file(self, json_data, the_file_name):
        if not json_data and the_file_name:
           json_data = self.parse_data_from_pdf(the_file_name)
           the_file_name = json_data.get("unique_id")
        return json_output_generator(json_data=json_data, the_file_name=the_file_name)

    def operate_pdf_content_collector(self):
        file_name = self.download_pdf_file()
        if file_name:
            parsed_data = self.parse_data_from_pdf(file_name)
            if parsed_data:
                self.display(data=parsed_data)
                self.write_content_to_json_file(json_data=parsed_data, the_file_name=f"{file_name}.pdf")
        return True


if __name__ == "__main__":
    pdf_links = [
        "https://www.lazardassetmanagement.com/docs/product/-sp10-/137/lazardonjapan_2023q3.pdf"
    ]
    for _ in pdf_links:
        PDFops(the_url=_).operate_pdf_content_collector()