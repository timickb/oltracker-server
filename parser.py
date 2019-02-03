from bs4 import BeautifulSoup
import yaml
import requests

class Parser:
    def __init__:
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
            'LSF': '%5B16%5D', # обж
            'Social': '%5B9%5D',
            'Literature': '%5B2%5D',
            'Ecology': '%5B21%5D',
            'PictureArt': '%5B22%5D',
            'PE': '%5B19%5D',
            'Law': '%5B15%5D', # право
            'Linguistics': '%5B24%5D',
            'Robotics': '%5B27%5D',
            'Drafting': '%5B31%5D', # черчение
            'Enterprise': '%5B23%5D' # предпринимательство
            'Economy': '%5B14%5D',
            'Foreign': '%5B0%5D',
            'Technology': '%5B17%5D',
            'Psychology': '%5B28%5D'
        }
    def getOlympiadsList(type_='any', subjects=[], period='year', period_date='', class_='any'):
        url = self.URL + 'type={}&class={}&period={}&period_date={}'.format(type_, class_, period, period_date)
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        return soup.prettify()

        
