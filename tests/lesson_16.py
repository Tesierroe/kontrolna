import logging
import os

import pytest
from work import FileAnalyzer

from tests.functions import check_link_with_mail, read_links_from_file, get_response_status_code, \
    check_if_links_exist, count_links_in_file, get_links_from_file, link_contains_uppercase


# Test for the absence of an empty link or path
@pytest.mark.regression
def test_non_empty_link_or_path():
    file_path = "https://google.com"
    FileAnalyzer(file_path)

    assert file_path.strip() != ""


# Test for the existence of 'valid_links.txt' and 'broken_links.txt' files
@pytest.mark.smoke
def test_files_are_created():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    assert os.path.exists("valid_links.txt")
    assert os.path.exists("broken_links.txt")


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


# Tests for the presence of a link with 'mail' in 'valid_links.txt' or 'broken_links.txt' files
def test_link_with_mail():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    assert check_link_with_mail("valid_links.txt") or check_link_with_mail("broken_links.txt")


# Test for 'valid_links.txt' containing only links with response status code 200
@pytest.mark.regression
def test_valid_links_with_status_code_200():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    valid_links = read_links_from_file("valid_links.txt")
    status_codes = [get_response_status_code(link) for link in valid_links]

    assert all(code == 200 for code in status_codes)


# Test for the absence of any links in 'valid_links.txt' or 'broken_links.txt' files
@pytest.mark.regression
def test_no_links_saved():
    file_path = "https://googjhgle.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    assert not check_if_links_exist("valid_links.txt")
    assert not check_if_links_exist("broken_links.txt")


# Test for the valid ending of the link or path
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


# Test for the absence of uppercase letters in the links of 'broken_links.txt' file
@pytest.mark.regression
def test_links_lowercase():
    file_path = "https://google.com"
    analyzer = FileAnalyzer(file_path)
    analyzer.analyze_file()

    broken_links = get_links_from_file("broken_links.txt")
    assert not any(link_contains_uppercase(broken_links))


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


def teardown(self):
    os.remove("valid_links.txt")
    os.remove("broken_links.txt")
    logging.info('\nTC session files are cleared \n')
