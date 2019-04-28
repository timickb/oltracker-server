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
        self.TYPEWORDS  = ['очная', 'личная', 'конференция', 'заочная', 'все типы']
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

        if 'тип' in result['subjects'][0]:
            result['subjects'] = []
            for typeword in self.TYPEWORDS:
                if typeword in result['subjects']:
                    subjects.append(typeword)
        
        if len(result['subjects']) == 0:
            result['subjects'].append('Любой предмет')


        eventID = int(link_raw['href'].split('/')[-1])
        result['id'] = eventID
        result['infourl'] = url

        print('='*30)
        print('Parsing event ' + str(eventID) + ', ' + url)

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
                classes_raw = item.find_all('td')[1].text
                if ',' in classes_raw:
                	classes_raw = classes_raw.split(',')
                else:
                	classes_raw = classes_raw.split('-')
                classes = []
                for i in range(int(classes_raw[0]), int(classes_raw[-1])+1):
                    classes.append(i)
                result['classes'] = classes
            elif name == 'Ссылка':
                result['link'] = item.find_all('td')[1].find('a')['href']
        
        return result


    def get_next_events(self, subject=-1, schclass=-1):
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