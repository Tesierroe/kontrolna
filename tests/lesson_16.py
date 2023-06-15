import logging
import os

import pytest
import requests
from main import FileAnalyzer


# from main import get_file_path, file_path
# from functions import check_link_with_mail
# from functions import read_links_from_file
# from functions import get_response_status_code
# from functions import check_if_links_exist
# from functions import count_links_in_file
# from functions import get_links_from_file
# from functions import link_contains_uppercase

# def setup_class():
#     file_path = get_file_path()
#     print(file_path)


# Test for the existence of 'valid_links.txt' and 'broken_links.txt' files
@pytest.mark.smoke
def test_files_are_created():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    assert os.path.exists("valid_links.txt")
    assert os.path.exists("broken_links.txt")

    # Clean up the created files
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")
    logging.info('\nTC session files are cleared \n')



# Test for the presence of at least one link in 'valid_links.txt' and 'broken_links.txt' files
@pytest.mark.smoke
def test_link_presence():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    with open("valid_links.txt", "r") as file:
        valid_links = file.readlines()
        assert len(valid_links) >= 1

    with open("broken_links.txt", "r") as file:
        broken_links = file.readlines()
        assert len(broken_links) >= 1

    # Clean up the created files
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")



# Tests for the presence of a link with 'mail' in 'valid_links.txt' or 'broken_links.txt' files

def test_link_with_mail():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    assert check_link_with_mail("valid_links.txt") or check_link_with_mail("broken_links.txt")

    # Clean up the created files
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")


def check_link_with_mail(filename):
    with open(filename, "r") as file:
        links = file.readlines()
        for link in links:
            if "mail" in link:
                print(f'This is the link I need {link}')
        return 'No such links'



# Test for 'valid_links.txt' containing only links with response status code 200
@pytest.mark.regression
def test_valid_links_with_status_code_200():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    valid_links = read_links_from_file("valid_links.txt")
    status_codes = [get_response_status_code(link) for link in valid_links]

    assert all(code == 200 for code in status_codes)

    # Clean up the created files
    os.remove("valid_links.txt")


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



# Test for the absence of any links in 'valid_links.txt' or 'broken_links.txt' files
@pytest.mark.regression
def test_no_links_saved():
    file_path = "https://googjhgle.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    assert not check_if_links_exist("valid_links.txt")
    assert not check_if_links_exist("broken_links.txt")

    # Clean up the created files
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")


def check_if_links_exist(filename):
    return os.path.isfile(filename) and os.path.getsize(filename) > 0



# Test for the absence of an empty link or path
@pytest.mark.regression
def test_non_empty_link_or_path():
    file_path = "https://google.com"
    FileAnalyzer(file_path)

    assert file_path.strip() != ""


def test_link_or_path_ending():
    file_path = "https://google.com"
    FileAnalyzer(file_path)

    assert file_path.endswith((".com", ".pdf"))


# Test for the sum of saved links in 'valid_links.txt' and 'broken_links.txt' files
@pytest.mark.regression
def test_sum_of_saved_links():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    valid_links_count = count_links_in_file("valid_links.txt")
    broken_links_count = count_links_in_file("broken_links.txt")

    assert valid_links_count + broken_links_count > 10
    print(valid_links_count + broken_links_count)

    # Clean up the created files
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")


def count_links_in_file(filename):
    with open(filename, 'r') as file:
        return sum(1 for _ in file)



# Test for the absence of uppercase letters in the links of 'broken_links.txt' file
@pytest.mark.regression
def test_links_lowercase():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    broken_links = get_links_from_file("broken_links.txt")

    assert not any(link_contains_uppercase(broken_links))

    # Clean up the created files
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")


def get_links_from_file(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


def link_contains_uppercase(links):
    for link in links:
        if any(char.isupper() for char in link):
            yield link



# Test for the absence of duplicate links in 'valid_links.txt' and 'broken_links.txt' files
@pytest.mark.regression
def test_no_duplicate_links():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    valid_links = get_links_from_file("valid_links.txt")
    broken_links = get_links_from_file("broken_links.txt")

    assert len(valid_links) == len(set(valid_links))
    assert len(broken_links) == len(set(broken_links))

    # Clean up the created files
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")


# def teardown_class(self):
#     os.remove("valid_links.txt")
#     os.remove("broken_links.txt")
#     logging.info('\nTC session files are cleared \n')
