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
from tri_helper import *


def main():
    # years = [str(year) for year in range(2015, 2019)]
    years = ['2018']
    genders = ['F', 'M']
    age_groups = [str(age) + '-' + str(age + 4) for age in range(25, 86, 5)]
    age_groups = ['18-24'] + age_groups

    for year in years:
        df = pd.DataFrame()
        for gender in genders:
            for age_group in age_groups:
                pages = 10
                num_page = check_num_pages(pages, year, gender, age_group)
                print("Total number of pages =", num_page, 'age=', age_group, 'gender=', gender)

                if num_page > 0:
                    data = get_yearly_record(year, gender, age_group, num_page)
                    df = df.append(data)
                else:
                    print('No Record for this age group!')

            print('Done, gender=', gender, 'age group=', age_group)
        print('Done for year', year)

        save_name = 'tri_santa_cruz_' + str(year) + '.csv'
        df.to_csv(save_name, index=False)


if __name__ == "__main__":
    main()
