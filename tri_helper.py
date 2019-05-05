"""
Author: Donghua (Lyla) Cai
Date: Apr 26, 2019
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd
import numpy as np
import copy


def check_num_pages(pages, year, gender, age_group):
    """
    Give a page number
    Return the last page number that we will have a table
    """

    page = pages
    table = None
    while (not table) and (page >= 0):
        url = 'http://www.ironman.com/triathlon/events/americas/ironman-70.3/santa-cruz/results.aspx?p=' + \
              str(page) + '&race=santacruz70.3&agegroup=' + str(age_group) + '&sex=' + str(gender) + \
              '&y=' + str(year) + '&ps=20#axzz5mVyaYOFb'
        html = urlopen(url)
        
        bs = BeautifulSoup(html.read(), 'lxml')
        table = bs.find('table', {'id': 'eventResults'})
        if table is not None:
            break
        else:
            page -= 1

    return page


def scrape_table(url, gender, age_group):
    """
    Given a url with corresponding gender, age_group
    Return the table of that webpage
    """
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')

    tr = bs.find_all('tr')
    record_list = []
    for ii in range(1, len(tr)):
        tds = tr[ii].find_all('td')
        record = [txt.text for ii, txt in enumerate(tds)]
        record += [gender, age_group]
        record_list.append(record)

    return record_list


def get_header(url):
    """
    Get the table header
    """
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')

    table_header = bs.find("thead").find_all("th")

    header = []
    for txt in table_header:
        name = txt.a.contents[0].replace(" ", "")
        header.append(name)

    return header


def get_yearly_record(year, gender, age_group, num_page):
    """
    Given a year, gender, age_group
    Return all the table data 
    """
    record = []

    for page in range(1, num_page + 1):
        print(page)

        url = 'http://www.ironman.com/triathlon/events/americas/ironman-70.3/santa-cruz/results.aspx?p=' + \
              str(page) + '&race=santacruz70.3&agegroup=' + str(age_group) + '&sex=' + str(gender) + \
              '&y=' + str(year) + '&ps=20#axzz5mVyaYOFb'

        data = np.array(scrape_table(url, gender, age_group))

        if page == 1:
            record = copy.deepcopy(data)
        else:
            record = np.concatenate((record, data))

    # Get header from dataframe
    url = 'http://www.ironman.com/triathlon/events/americas/ironman-70.3/santa-cruz/results.aspx?rd=' + \
              str(year) + '#axzz5mVyaYOFb'
    header = get_header(url)
    header += ['Gender', 'AgeGroup']

    df = pd.DataFrame(record, columns=header)
    return df
