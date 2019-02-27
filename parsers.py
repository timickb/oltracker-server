from bs4 import BeautifulSoup as bs
import yaml
import requests
import re

# TODO парсер для ресурса http://moeobrazovanie.ru
class MoeObr():
    def __init__(self):
        self.SERVER = 'https://moeobrazovanie.ru'
        self.BASE_URL = 'https://moeobrazovanie.ru/olimpiady.php?predmet={}&klass={}&data={}&sort=date&page={}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        self.ITEMS_ON_PAGE = 20
        self.info_table_rows = ['scale', 'level', 'type', 'classes', 'deadlines', 'subjects', 'places', 'rounds', 
        'awardee_def', 'privileges', 'registration', 'site', 'orgs']

        self.subjects = {
            "all": -1,
            "mathematics": "matematika",
            "russian": "russkii_yazyk",
            "informatics": "informatika",
            "physics": "fizika",
            "chemistry": "himiya",
            "biology": "biologiya",
            "social": "obschestvoznanie",
            "literature": "literatura",
            "geography": "geografiya",
            "foreign": "inostrannyi_yazyk",
            "art": "iskusstvo",
            "economy": "ekonomika"
        }
    
    def getList(self, subject="all", class_=-1, date=-1):
        try:
            subject = self.subjects[subject]
        except:
            subject = -1
        result = []
        # make url for this query
        url = self.BASE_URL.format(subject, class_, date, 1)

        # make request
        session = requests.Session()
        request = session.get(url, headers=self.headers)

        if request.status_code == 200:
            # if success, parse the result
            soup = bs(request.content, 'html.parser')

            # get an amount of found items
            amount = int(soup.find('b', class_='ml10').text)
            if amount == 0:
                return '0'
            # calculate number of pages
            pages_amount = amount // self.ITEMS_ON_PAGE
            if amount % self.ITEMS_ON_PAGE > 0:
                pages_amount += 1
            
            # get elements
            raw_elements = soup.find_all('div', class_='OSROlyRow')
            for i in range(len(raw_elements)):
                result.append(self.getDictFromData(raw_elements[i]))
            

            # get other pages
            if pages_amount > 1:
                for j in range(2, pages_amount+1):
                    # make query for new page
                    url = self.BASE_URL.format(subject, class_, date, j)
                    request = session.get(url, headers=self.headers)
                    soup = bs(request.content, 'html.parser')
                    # get elements
                    raw_elements = soup.find_all('div', class_='OSROlyRow')
                    for i in range(len(raw_elements)):
                        result.append(self.getDictFromData(raw_elements[i]))
            
        else:
            return 'error'
        return result
    
    def get_subjects_from_string(self, string):
        first = re.sub("^\s+|\n|\r|\s+$", '', string)
        return first.split(', ')

    def get_classes_from_string(self, string):
        first = string.split(' | ')[0]
        second = re.sub("^\s+|\n|\r|\s+$", '', first)
        third = second.split(' классы')[0]
        return third.split(', ')
    
    def get_start_date_from_string(self, string):
        first = string.split(' - ')
        second = re.sub("^\s+|\n|\r|\s+$", '', first[0])
        return second
    
    def get_end_date_from_string(self, string):
        first = string.split(' - ')
        second = re.sub("^\s+|\n|\r|\s+$", '', first[1])
        return second
    
    def get_site_by_link(self, string):
        html = requests.get(self.SERVER + string).content
        soup = bs(html, 'html.parser')
        table = soup.find('table', class_='oly_table')
        table.find('table', class_='oly_search_block').decompose()

        url = ''
        links = table.find_all('a')
        url = links[-2]['href']
        return url
    
    def getDictFromData(self, item):
        olympiad = {}

        # parse title
        title_obj = item.find('a', class_='olyTtl')
        olympiad['title'] = title_obj.text

        # decompose rubbish
        title_obj.decompose()
        spans = item.find_all('span')
        for span in spans:
            span.decompose()

        # parse organisators
        orgs_raw = item.find_all('a')
        orgs = []
        for org in orgs_raw:
            orgs.append(org.text)

        # decompose rubbish
        item.find('div').decompose()

        # parse subjects and classes
        item_text = item.text.split(':')
        olympiad['subjects'] = self.get_subjects_from_string(item_text[1])
        olympiad['classes'] = self.get_classes_from_string(item_text[2])
        olympiad['date_start'] =  self.get_start_date_from_string(item_text[3])
        olympiad['date_end'] =  self.get_end_date_from_string(item_text[3])
        olympiad['orgs'] = orgs
        

        return olympiad