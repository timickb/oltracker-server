from bs4 import BeautifulSoup as bs
import yaml
import requests
import re

class OlympiadaRu():
    def __init__(self):
        self.SERVER = 'https://info.olimpiada.ru'
        self.BASE_URL_CURRENT='https://info.olimpiada.ru/current/page/{}?subject%5B{}%5D=on&class%5B{}%5D=on&dtype%5B{}%5D=on'
        self.BASE_URL_NEXT = 'https://info.olimpiada.ru/events/page/{}?subject%5B{}%5D=on&class%5B{}%5D=on&type%5B{}%5D=on'
        self.HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        self.NUMBERS = ['first', 'second', 'third', 'forth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
        self.KEYWORDS = ['финал', 'Финал', 'Заключительн', 'заключительн']
        with open('matches.yml', 'r', encoding='utf-8') as file:
            try:
                matches = yaml.load(file)
                self.SUBJECTS = matches['subjects-olru']
                self.TYPES = matches['types-olru']
            except:
                print('Ooops...')
                exit(1)
    
    def handle_event(self, row):
        result = {}
        link_raw = row.find_all('td')[1].find('a')
        url = self.SERVER + link_raw['href']
        result['title'] = link_raw.text

        result['stage'] = 'selection'
        for keyword in self.KEYWORDS:
            if keyword in result['title']:
                result['stage'] = 'final'
                break

        subjects_raw = row.find('div', class_='div_selected_subjects')
        subjects = []
        if subjects_raw != None:
            subjects_spans = subjects_raw.find_all('span')
            for item in subjects_spans:
                subjects.append(item.text)
        else:
            try:
                subjects_raw = row.find('span', class_='span_filtered')
                subjects.append(subjects_raw.text.split(' | ')[2])
            except:
                subjects.append(row.find_all('td')[1].text.split(' | ')[1])
        result['subjects'] = subjects

        eventID = int(link_raw['href'].split('/')[-1])
        result['id'] = eventID
        result['infourl'] = url

        print('='*30)
        print('Parsing event ' + str(eventID))

        request = requests.get(url, headers=self.HEADERS)
        soup = bs(request.content, 'html.parser', from_encoding='utf-8')

        data = soup.find('div', class_='main')
        deadlines_raw = data.find('font')
        result['date_start'] = deadlines_raw.text.split(' - ')[0]
        try:
            result['date_end'] = deadlines_raw.text.split(' - ')[1]
        except:
            result['date_end'] = result['date_start']
        info_table = data.find('table', class_='event_info_table')
        info_table_rows = info_table.find_all('tr')
        for item in info_table_rows:
            name = item.find_all('td')[0].text
            if name == 'Классы':
                classes_raw = item.find_all('td')[1].text.split('-')
                classes = []
                for i in range(int(classes_raw[0]), int(classes_raw[-1])+1):
                    classes.append(i)
                result['classes'] = classes
            elif name == 'Ссылка':
                result['link'] = item.find_all('td')[1].find('a')['href']
        
        return result


    def get_next_events(self, subject=-1, schclass=-1):
        ITEMS_ON_PAGE = 20
        result = []
        if schclass == -1: schclass='%'

        url = self.BASE_URL_NEXT.format(1, self.SUBJECTS[str(subject)], schclass, self.TYPES['-1'])

        # make request
        session = requests.Session()
        request = session.get(url, headers=self.HEADERS)

        if request.status_code == 200:
            soup = bs(request.content, 'html.parser', from_encoding='utf-8')
            elements = []
            for i in range(10):
                try:
                    ul = soup.find('ul', class_=self.NUMBERS[i])
                    elements += ul.find_all('li')
                except:
                    pass            
            if len(elements) == 0:
                return result
            for item in elements:
                if item.find('table') != None:
                    result.append(self.handle_event(item.find('tr')))
            
            counter = soup.find('ul', {'id': 'counter'})

            if counter != None:
                pages_amount = int(counter.find_all('li')[-2].find('a').text)
                print(pages_amount)
                for i in range(2, pages_amount+1):
                    url = self.BASE_URL_NEXT.format(i, self.SUBJECTS[str(subject)], schclass, self.TYPES['-1'])
                    request = session.get(url, headers=self.HEADERS)
                    soup = bs(request.content, 'html.parser', from_encoding='utf-8')
                    rows = []
                    elements = []
                    for i in range(10):
                        try:
                            ul = soup.find('ul', class_=self.NUMBERS[i])
                            elements += ul.find_all('li')
                        except:
                            pass
                    for item in elements:
                        if item.find('table') != None:
                            rows.append(item.find('tr'))
                    for row in rows:
                        result.append(self.handle_event(row))
        return result
            


    def get_current_events(self, subject=-1, schclass=-1, oltype=-1):
        ITEMS_ON_PAGE = 20
        result = []
        if schclass == -1: schclass = '%'

        url = self.BASE_URL_CURRENT.format(1, self.SUBJECTS[str(subject)], schclass, self.TYPES[str(oltype)])

        # make request
        session = requests.Session()
        request = session.get(url, headers=self.HEADERS)

        if request.status_code == 200:
            soup = bs(request.content, 'html.parser', from_encoding='utf-8')
            table = soup.find('table', {'style': 'margin-left:40px'})
            rows = table.find_all('tr')
            if len(rows) == 0:
                return result
            for row in rows:
                result.append(self.handle_event(row))

            counter = soup.find('ul', {'id': 'counter'})
            if counter != None:
                pages_amount = int(counter.find_all('li')[-2].find('a').text)
                for i in range(2, pages_amount+1):
                    url = self.BASE_URL_CURRENT.format(i, self.SUBJECTS[str(subject)], schclass, self.TYPES[str(oltype)])
                    request = session.get(url, headers=self.HEADERS)
                    soup = bs(request.content, 'html.parser', from_encoding='utf-8')
                    table = soup.find('table', {'style': 'margin-left:40px'})
                    rows = table.find_all('tr')
                    for row in rows:
                        result.append(self.handle_event(row))

        session.close()
        return result





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
    
    def get_elementst(self, subject="all", class_=-1, date=-1):
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
            soup = bs(request.content, 'html.parser', from_encoding='utf-8')

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
                result.append(self.get_dict_from_data(raw_elements[i]))
            

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
                        result.append(self.get_dict_from_data(raw_elements[i]))
            
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
        print('='*30)
        for link in links:
            if link['href'].startswith('http://'):
                url = link['href']
                break
        if url == '':
            url = 'undefined'
        return url
    
    def get_dict_from_data(self, item):
        olympiad = {}

        # parse title
        title_obj = item.find('a', class_='olyTtl')
        olympiad['title'] = title_obj.text

        #parse link
        olympiad['link'] = self.get_site_by_link(title_obj['href'])

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
        
        print('Parsed:', olympiad['title'])

        return olympiad