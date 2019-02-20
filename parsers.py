from bs4 import BeautifulSoup as bs
import yaml
import requests

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
    
    def getList(self, subject=-1, class_=-1, date=-1):
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

            raw_elements = soup.find_all('div', class_='OSROlyRow')
            for i in range(len(raw_elements)):
                result.append(self.getDictFromData(raw_elements[i]))
            
            print(result)
            
        else:
            return 'error'
    
    def getDictFromData(self, data):
        # get info page
        page_url = self.SERVER + data.find('a')['href']
        request = requests.get(page_url, headers=self.headers)
        if request.status_code != 200:
            return 'error'
        info_page = request.content

        # forming output data
        result = {
            'title': 'undefined',
            'deadlines': 'undefined',
            'orgs': 'undefined',
            'subjects': [],
            'classes': [],
            'places': 'undefined'
        }

        # fetch a title
        result['title'] = data.find('a', class_='olyTtl').text

        #fetch information from its page
        oly_table_rows = info_page.find('table', class_='oly_table').find_all('tr')

        return result


# TODO парсер для ресурса http://olimpiada.ru
class OlimpiadaRu():
    def __init__(self):
        self.URL = 'https://olimpiada.ru/activities/?'
        self.SUBJECTS = {
            'Math': '%5B6%5D',
            'Informatics': '%5B7%5D',
            'Physics': '%5B12%5D',
            'Chemistry': '%5B13%5D',
            'Biology': '%5B11%5D',
            'Geography': '%5B10%5D',
            'History': '%5B8%5D',
            'Russian': '%5B1%5D',
            'Astronomy': '%5B20%5D',
            'Art': '%5B18%5D',
            'LSF': '%5B16%5D',
            'Social': '%5B9%5D',
            'Literature': '%5B2%5D',
            'Ecology': '%5B21%5D',
            'PictureArt': '%5B22%5D',
            'PE': '%5B19%5D',
            'Law': '%5B15%5D',
            'Linguistics': '%5B24%5D',
            'Robotics': '%5B27%5D',
            'Drafting': '%5B31%5D',
            'Enterprise': '%5B23%5D',
            'Economy': '%5B14%5D',
            'Foreign': '%5B0%5D',
            'Technology': '%5B17%5D',
            'Psychology': '%5B28%5D'
        }
    def getList(self, type_='any', subjects=[], period='year', period_date='', class_='any'):
        pass
