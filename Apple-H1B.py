# Apple Careers - H1B - app-post.net

from email import header
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


roles_needed = []
NOF_list = []
salaries = []
dates_posted = []
date_ranges = []
locations = []
posting_urls = []

postings = []


def get_html_from(page):
    """ Returns the HTML code from the website. """

    print('Scraping data from page:', page)
    url = f'https://app-post.net/index.php/page/{page}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'The returned status code is: {response.status_code}')
    print('Status code:', response.status_code)

    soup = BeautifulSoup(response.text, 'lxml')
    print('Returned soup.\n')

    return soup
            

def get_offline_text(soup):
    """ Creates a file of HTML code that will be used for offline parsing. """

    with open('Apple-H1B.html', 'w') as file:
        file.write(str(soup))
        # print('File saved for offline parsing.')


def roles_available(soup):
    """ Returns the role needed. """

    sections = soup.find_all('div', class_='entry-column')

    try: 
        position_pattern_1 = r"position of[^.]*"
        position_pattern_2 = r"classification of[^.]*"

        for item in sections: 
            str_position = str(item)

            position_1 = re.finditer(position_pattern_1, str_position)
            position_2 = re.finditer(position_pattern_2, str_position)

            for i in position_1: 
                try:
                    role = i.group(0)
                    role = role.replace('position of ', '').replace('<br/>4', '').replace('&amp; ', '&')
                    roles_needed.append(role)
                except:
                    role = '----'
                    roles_needed.append(role)


            for i in position_2: 
                try:
                    role = i.group(0)
                    role = role.replace('classification of ', '').replace('<br/>4', '').replace('&amp; ', '&')
                    roles_needed.append(role)
                except:
                    role = '----'
                    roles_needed.append(role)

    except: 
        print('Cannot find this position pattern.')


def find_filings(soup): 
    """ Returns the "Notice Of Filing listing number" for each position. """

    sections = soup.find_all('div', class_='entry-column')

    for item in sections:
        try:
            notice_of_filing = item.find('h2', class_='entry-title post-title').text
            notice_of_filing = notice_of_filing.lower().replace('noticeoffiling c#', '').replace('notice of filing #', '')
            notice_of_filing = notice_of_filing.replace('nof c#', '').replace('Notice of Filing #', '')
            notice_of_filing = notice_of_filing.replace('lca nof patil sagar', '----').replace('notice of filing c#', '')
            notice_of_filing = notice_of_filing.strip().replace('noticeoffilinf c#', '').replace('notice of filing case # ', '')
            notice_of_filing = notice_of_filing.replace('notice of fililng #', '').replace('noticeoffiling ', '')
            notice_of_filing = notice_of_filing.replace('nof case # ', '').replace('notice of filing#', '')
            notice_of_filing = notice_of_filing.replace('notice of filing wegrzynski michal', '----')
            NOF_list.append(notice_of_filing)
        except:
            notice_of_filing = '----'
            NOF_list.append(notice_of_filing)


def find_salaries(soup):  
    """ Returns the salary of each position. """


    # pattern_money = r"\$\d+,*\d+.per"
    # pattern_money = r"\$\d+,*\d+(\.00)?.per"
    pattern_money = r"\$\s?\d+,*\d+(\.00)?.per"

    content = soup.find_all('div', 'entry-content')

    if pattern_money: 

        for item in content:
            str_obj = str(item)

            money = re.finditer(pattern_money, str_obj)

            for i in money: 
                try:
                    money = i.group(0)
                    money = money.replace(',', '').replace('per', '')
                    salaries.append(money)
                except: 
                    money = '----'
                    salaries.append(money)


def find_dates_posted(soup):  
    """ Returns the date each position was posted on. """

    sections = soup.find_all('div', class_='entry-column')

    for date in sections: 
        try:
            date_posted = date.find('time', 'timestamp updated').text
            dates_posted.append(date_posted)
        except:
            date_posted = '----'
            dates_posted.append(date_posted)
         

def dates_needed(soup):
    """ Returns the date range for each position. """

    sections = soup.find_all('div', class_='entry-column')

    try: 
        date_range_pattern = r"sought is[^.]*"

        for dates in sections: 
            str_dates = str(dates)
            date_range = re.finditer(date_range_pattern, str_dates)
            for i in date_range: 
                try:
                    date = i.group(0)
                    date = date.replace('sought is ', '').replace('/', '-')
                    date_ranges.append(date)
                except:
                    date = '----'
                    date_ranges.append(date)

    except:
        print('Cannot find date range pattern.')


def job_location(soup):
    """ Returns the location of each position. """

    sections = soup.find_all('div', class_='entry-column')

    try: 
        location_pattern = r"will occur in[^.]*"

        for location in sections:
            str_location = str(location)
            location_areas = re.finditer(location_pattern, str_location)
            for i in location_areas:
                try: 
                    location = i.group(0)
                    location = location.replace('will occur in', '').replace('<br/>7', '').strip()
                    locations.append(location)
                except: 
                    location = '----'
                    locations.append(location)

    except:
        print('Cannot find location pattern.')


def posting_url(soup):   
    """ Returns the URL for the individual posting. """

    sections = soup.find_all('div', class_='entry-column')

    for url in sections: 
        try: 
            individual_url = url.find('a')['href']
            posting_urls.append(individual_url)
        except: 
            individual_url = '----'
            posting_urls.append(individual_url)
           

def info():
    """ Constructs dictionaries after iterating through lists. """
    for (job_role, filing, salary, date_posted, needed_date, location, posting_url) in zip(roles_needed, NOF_list, salaries, dates_posted, date_ranges, locations, posting_urls):

        job = {
            'job_role':  job_role,
            'filing': filing,
            'salaries': salary, 
            'date_posted': date_posted,
            'needed_date_range': needed_date,
            'location': location,
            'posting_url': posting_url,
        }

        print(f'Getting info for {job_role}')
        postings.append(job)


def output():
    """ Outputs the data into a CSV file. """
    
    df = pd.DataFrame(postings)
    df.to_csv('Apple-H1B-Postings.csv')
    print('\nInformation saved to CSV file.')



if __name__ == '__main__':

    for page in range(1, 5):
        soup = get_html_from(page)
        get_offline_text(soup)
        roles_available(soup)
        find_filings(soup)
        find_salaries(soup)
        find_dates_posted(soup)
        dates_needed(soup)
        job_location(soup)
        posting_url(soup)
        
    info()
    output()
    print('\n-----FINISHED-----\n')
