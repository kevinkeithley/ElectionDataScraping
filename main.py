import os
from datetime import datetime
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

states = ['Alabama',
          'Alaska',
          'Arizona',
          'Arkansas',
          'California',
          'Colorado',
          'Connecticut',
          'Delaware',
          'District of Columbia',
          'Florida',
          'Georgia',
          'Hawaii',
          'Idaho',
          'Illinois',
          'Indiana',
          'Iowa',
          'Kansas',
          'Kentucky',
          'Louisiana',
          #'Maine',
          'Maryland',
          'Massachusetts',
          'Michigan',
          'Minnesota',
          'Mississippi',
          'Missouri',
          'Montana',
          #'Nebraska',
          'Nevada',
          'New Hampshire',
          'New Jersey',
          'New Mexico',
          'New York',
          'North Carolina',
          'North Dakota',
          'Ohio',
          'Oklahoma',
          'Oregon',
          'Pennsylvania',
          'Rhode Island',
          'South Carolina',
          'South Dakota',
          'Tennessee',
          'Texas',
          'Utah',
          'Vermont',
          'Virginia',
          'Washington',
          'West Virginia',
          'Wisconsin',
          'Wyoming']


def scrape(path, state_list):
    # Set up chrome webdriver
    driver = webdriver.Chrome(path)

    # Loop through selected states
    for s in state_list:
        # Load site
        site_url = 'https://www.nbcnews.com/politics/2020-elections/' + s.lower().replace(' ', '-') + '-president-results'
        driver.get(site_url)

        # Check for button to expand data list to full
        if len(driver.find_elements_by_xpath('//span[text()="Show all Counties"]')) > 0:
            button_text = driver.find_element_by_xpath('//span[text()="Show all Counties"]')
            button = button_text.find_element_by_xpath('./../..')
            button.send_keys(Keys.ENTER)

        # Find web element that contains county names, create list
        counties = driver.find_elements_by_class_name('pr9')
        county_list = []
        for c in counties:
            county_list.append(c.text)
        county_list = remove_empty_strings(county_list)

        # Find web element that contains candidate names, create list
        candidates = driver.find_elements_by_class_name('dib-m')
        candidate_list = []
        for c in candidates:
            candidate_list.append(c.text.title())
        candidate_list = remove_empty_strings(candidate_list)

        # Find web element that contains votes for candidates, create list
        votes = driver.find_elements_by_class_name('pr5')
        vote_list = []
        for v in votes:
            vote_list.append(v.text)
        vote_list = remove_empty_strings(vote_list)

        # Create data structure
        chunk = len(county_list)
        state = [s] * chunk
        data = [state, county_list]
        # Split list of votes into list for each candidate by using number of counties
        for i in range(len(candidate_list)):
            seq_start = chunk*i
            seq_end = chunk*i + chunk
            data.append(vote_list[seq_start:seq_end])
        # Transpose array to use for data frame
        array = np.array(data)
        transpose = array.T
        transpose_list = transpose.tolist()
        # Create data frame
        col_names = ['State'] + ['County'] + candidate_list
        df = pd.DataFrame(transpose_list, columns=col_names)

        # Create 'Data' directory
        cwd = os.getcwd()
        if not os.path.exists('Data'):
            os.makedirs('Data')
        os.chdir('Data')
        # Create 'Data' subdirectory, by M-D-Y
        now = datetime.now()
        date_str = now.strftime('%m-%d-%y')
        if not os.path.exists(date_str):
            os.makedirs(date_str)
        os.chdir(date_str)
        # Save data frame to csv as *State*.csv
        df.to_csv(s.replace(' ', '') + '.csv', index=False)
        os.chdir(cwd)


def remove_empty_strings(lst):
    return [i for i in lst if i]


if __name__ == '__main__':
    scrape('C:\Program Files (x86)\chromedriver.exe',
           states)