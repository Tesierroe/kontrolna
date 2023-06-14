import os
import requests

# не виходить заімпортити усі функції
# ModuleNotFoundError: No module named 'functions'

def check_link_with_mail(filename):
    with open(filename, "r") as file:
        links = file.readlines()
        for link in links:
            if "mail" in link:
                print(f'This is the link I need {link}')
        return 'No such links'


def read_links_from_file(filename):
    with open(filename, "r") as file:
        links = file.readlines()
        return [link.strip() for link in links]


def get_response_status_code(link):
    try:
        response = requests.get(link)
        return response.status_code
    except requests.exceptions.RequestException:
        return None


def check_if_links_exist(filename):
    return os.path.isfile(filename) and os.path.getsize(filename) > 0


def count_links_in_file(filename):
    with open(filename, 'r') as file:
        return sum(1 for _ in file)


def get_links_from_file(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


def link_contains_uppercase(links):
    for link in links:
        if any(char.isupper() for char in link):
            yield link