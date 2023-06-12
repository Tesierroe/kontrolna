import argparse
import requests
import re
import logging
from PyPDF2 import PdfReader

logging.basicConfig(level=logging.INFO)


class FileAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze_file(self):
        if self.file_path.endswith('.pdf'):
            pdf_analyzer = PdfAnalyzer(self.file_path)
            pdf_analyzer.analyze_file()
        else:
            url_analyzer = UrlAnalyzer(self.file_path)
            url_analyzer.analyze_file()

    def save_links(self, links, filename):
        with open(filename, 'w+') as file:
            for link in links:
                file.write(link + '\n')


class UrlAnalyzer(FileAnalyzer):
    def analyze_file(self):
        links = self.get_links_from_url(self.file_path)
        self.process_links(links)

    @staticmethod
    def get_links_from_url(url) -> list:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
                return links
            else:
                logging.error(f'Failed to retrieve content from URL: {url}')
                return []
        except requests.exceptions.RequestException as e:
            logging.error(f'An error occurred while accessing URL: {url}')
            logging.error(e)
            return []

    @staticmethod
    def check_link(link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                print(f'Yep, the link {link} is valid')
                return True
            else:
                logging.info(f'The link {link} is NOT valid')
                return False
        except requests.exceptions.RequestException:
            logging.info(f'The link {link} is NOT valid')
            return False

    def process_links(self, links):
        valid_links = []
        broken_links = []
        for link in links:
            if self.check_link(link):
                valid_links.append(link)
            else:
                broken_links.append(link)
        self.save_links(valid_links, 'valid_links.txt')
        self.save_links(broken_links, 'broken_links.txt')

    def save_links(self, links, filename):
        with open(filename, 'w+') as file:
            for link in links:
                file.write(link + '\n')


class PdfAnalyzer(FileAnalyzer):
    def analyze_file(self):
        links = self.get_links_from_pdf(self.file_path)
        self.process_links(links)

    @staticmethod
    def get_links_from_pdf(pdf_path) -> list:
        links = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                page_links = re.findall(r'(https?:\/\/[\da-z\.-]+\.[a-z\.]{2,6}[\/\w\.-]*)\/?', page_text)
                links.extend(page_links)
        return links

    def process_links(self, links):
        valid_links = []
        broken_links = []
        for link in links:
            if self.check_link(link):
                valid_links.append(link)
            else:
                broken_links.append(link)
        self.save_links(valid_links, 'valid_links.txt')
        self.save_links(broken_links, 'broken_links.txt')

    @staticmethod
    def check_link(link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                print(f'Yep, the link {link} is valid')
                return True
            else:
                logging.info(f'The link {link} is NOT valid')
                return False
        except requests.exceptions.RequestException:
            logging.info(f'The link {link} is NOT valid')
            return False

    def save_links(self, links, filename):
        with open(filename, 'w+') as file:
            for link in links:
                file.write(link + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='file_analyzer', description='Tool for analyzing links in a PDF file or URL')
    parser.add_argument('-url', type=str, help='You can set URL for parsing')
    parser.add_argument('-pdf', type=str, help='Path to the PDF file')
    args = parser.parse_args()

    if args.url:
        analyzer = UrlAnalyzer(args.url)
        analyzer.analyze_file()
    elif args.pdf:
        analyzer = PdfAnalyzer(args.pdf)
        analyzer.analyze_file()
    else:
        file_path = input('Please set the full URL or path to the PDF file for parsing: ')
        print('Checking if the link is valid...')
        analyzer = FileAnalyzer(file_path)
        analyzer.analyze_file()
