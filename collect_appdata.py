import requests
from google_play_scraper import app
import csv
from bs4 import BeautifulSoup


def see_more_apps(html, lang, country):
    """
    Get a list of application IDs that are in the HTML of 'See More'
    page from the input HTML.

    Assume that the input HTML is an HTML of google play store and
    contains the 'See More' button.

    Args:
        html: A Beautifulsoup object containing the HTML structure.
        lang: A string refering to ISO 639-1 language code.
        country: A string refering to ISO 3166 country code.

    Returns:
        A list refering to the application IDs.
    """

    # Set two empty lists so that one can contain the urls of the 'See
    # More' page and another one can contain the IDs of the applications
    # obtained in the pages.
    see_more_urls = []
    new_ids = []

    # Find all of the element of the 'See More' button from the input HTML.
    see_mores = html.find_all('a', class_='U8Ww7d')

    # Get the urls of the 'See More' pages and put them into the list that
    # is defined previously.
    for see_more in see_mores:
        see_more_urls.append(f'{see_more.get("href")}&hl={lang}&gl={country}')

    # For each url of 'See More' page, fetch and inspect to get the
    # HTML. Then, get the IDs of the applications that are in the page.
    for url in see_more_urls:
        req = requests.get(f'https://play.google.com{url}')
        html = BeautifulSoup(req.content, 'html.parser')
        apps = html.find_all('a', class_='poRVub')

        # The application ID is in the href after '?id=', so find the
        # ID by taking the part of the url after it.
        for app in apps:
            id = app.get('href').split('?id=', 1)[1]
            new_ids.append(id)

    return new_ids


def get_app_info(single_id, lang, country, col):
    """
    Get information in the input set that describes the application
    using google play scrapper library.

    Assume that the id, language and the country code is correct.

    Args:
        single_id: A string of the ID of an application.
        lang: A string refering to the language of the app.
        country: A string refering to the country code of the app.
        col: A set containing the name of the columns of the
            information of the application.

    Returns:
        A dictionary that contains colummn name as the key and the
        information as the value.
    """
    # Get application information using 'app' function of the google
    # play scrapper library.
    info = app(single_id, lang, country)

    # Filter only the information that are in the input set containing
    # the name of the columns.
    filtered_info = {key: info[key] for key in info.keys() & col}

    return filtered_info


def find_ids(input_url, id_list=[], lang='en', country='US'):
    """
    Append application IDs from the input url to the input id list.

    Assume that the input url is a url of google play store and the
    HTML of it contains the 'See More' button. The list of ID is
    initially set to empty list, the language is set to English and the
    country is set to US if not defined.

    Args:
        input_url: A string refering to the url of
        id_list: A list of strings refering to the IDs of the
                applications.
        lang: A string refering to ISO 639-1 language code.
        country: A string refering to ISO 3166 country code.

    Returns:
        A list containing the application IDs.
    """

    # Fetch a page of given url to inspect it with BeautifulSoup
    # and get the HTML of it.
    start_page = requests.get(input_url)
    soup = BeautifulSoup(start_page.content, 'html.parser')

    # Define another list that is same as the input list to append
    # more IDs.
    new_idlist = id_list

    # Go to each web page that is directed from the 'See More' button
    # and get all the application IDs from the 'See More' page.
    new_ids = see_more_apps(soup, lang, country)

    # Append the IDs to the returning list if the ID doesn't exist
    # in the list.
    for ids in new_ids:
        if ids not in new_idlist:
            new_idlist.append(ids)

    return new_idlist


def collect_app_info(id_list, file_name, lang, country):
    """
    Create a csv file containing the information of the applications
    that are in the input list.

    Args:
        id_list: A list of strings refering to the IDs of applications.
        lang: A string refering to ISO 639-1 language code.
        country: A string refering to ISO 3166 country code.
        file_name: A string refering to the file name of the data.
    """

    # Create a set containing the name of the column of the information.
    col = {'title', 'free', 'score', 'price', 'contentRating',
           'genre', 'size'}

    # Set an empty list to hold the dictionaries of information of
    # each application.
    info = []

    # Append information in the empty list for each ID in the id list.
    for ids in id_list:
        info.append(get_app_info(ids, lang, country, col))

    # Write a csv file with the column name and the information in
    # the list with matching column, except the case when it can't
    # find the file name.
    try:
        with open(f'{file_name}.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=col)
            writer.writeheader()
            for single_info in info:
                writer.writerow(single_info)
    except IOError:
        print('I/O error')
