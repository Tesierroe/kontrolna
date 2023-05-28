import argparse
import requests
import re


class UrlAnalyzer:
    def __new__(cls, *args, **kwargs):
        analyzer = super().__new__(cls)
        if not args and not kwargs:
            analyzer.url = cls.user_input
        return analyzer

    def __init__(self, url=None):
        if url:
            self.url = url
        else:
            self.url = self.user_input()
        self.link_analyzer = LinkAnalyzer(self.url)

    @staticmethod
    def user_input():
        parse = argparse.ArgumentParser()
        parse.add_argument('-url', type=str, help='You can set url for parsing')
        args = parse.parse_args()
        if args.url:
            return args.url
        else:
            url = input('Please set full URL for parsing: ')
            return url

    def info_from_link(self):
        self.link_analyzer.check_link(self.url)

    def get_links_from_url(self, url) -> list:
        response = requests.get(url)
        if response.status_code == 200:
            links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
            return links
        else:
            print(f'Failed to retrieve content from URL: {url}')
            return []


class LinkAnalyzer:
    def __init__(self, url):
        self.url = url

    def check_link(self, link):
        try:
            get = requests.get(link)
            if get.status_code == 200:
                print(f'Yep, the link {link} is valid')
                return True
            else:
                print(f'The link {link} is NOT valid')
                return False
        except requests.exceptions.MissingSchema:
            print(f'The link {link} is NOT valid')
            return False

    def check_links(self, links):
        for link in links:
            self.check_link(link)

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
    def save_links(links, filename):
        with open(filename, 'w+') as file:
            for link in links:
                file.write(link + '\n')


if __name__ == "__main__":
    analyzer = UrlAnalyzer()
    print('Checking if the link is valid ..')
    analyzer.info_from_link()
    print('----------------------------------')

    print(f'Checking all links in {analyzer.url}')
    links = analyzer.get_links_from_url(analyzer.url)
    analyzer.link_analyzer.check_links(links)
    analyzer.link_analyzer.process_links(links)
