from bs4 import BeautifulSoup
import requests
from decimal import Decimal

class ImdbTitle():
    def __init__(self, url=None, title=None):
        self.url = None
        self.page_soup = None
        self.title = None

        if url != None:
            self.url = url
            self.get_title_from_url()

        if title != None:
            self.title = title
            self.get_url_from_title()


        self.title_name = ''
        self.ratings = 0.0
        self.genres = []
        self.plot_keywords = []
        self.plot_keywords_number = 5

        self.url_fullcredits = 'https://www.imdb.com/title/' + self.title + '/fullcredits'
        self.director = []
        self.writtenby = []
        self.cast_list = []
        self.cast_list_number = 5



        self.generate_page_soup()
        self.get_title()
        self.get_ratings()
        self.get_genres()
        self.get_plot_keywords()
        self.get_full_credits()


    def generate_page_soup(self):
        if self.url != None:
            page = requests.get(self.url)
            self.page_soup = BeautifulSoup(page.text, 'html.parser')
            return True
        else:
            return False

    def get_title_from_url(self):
        self.title = self.url.split('/')[4]
        return self.title

    def get_url_from_title(self):
        self.url = 'http://www.imdb.com/title/' + self.title
        return self.url

    def get_title(self):
        title_with_year = self.page_soup.select('h1')[0]
        title_with_year.find('span').decompose()
        self.title_name = title_with_year.text.strip()
        
        return self.title_name

    def get_ratings(self):
        rating_div = self.page_soup.find(class_='ratingValue')
        if rating_div is not None:
            self.ratings = Decimal(rating_div.strong.span.text.strip())
    
        return self.ratings

    def get_genres(self):
        all_div = self.page_soup.find_all(class_='see-more inline canwrap')

        for div in all_div:
            if div.h4.text.strip() == 'Genres:':
                genres = div.find_all('a')
                for genre in genres:
                    self.genres.append(genre.text.strip())
            else:
                div.decompose()

        return self.genres

    def get_plot_keywords(self):
        url = 'http://www.imdb.com/title/' + self.title + '/keywords'
        keywords_page = requests.get(url)
        if keywords_page.status_code == 200:
            keywords_page_soup = BeautifulSoup(keywords_page.text, 'html.parser')

            all_divs = keywords_page_soup.find_all(class_='sodatext')

            for div in all_divs:
                links = div.find_all('a')
                for link in links:
                    self.plot_keywords.append(link.text.strip())

        return self.plot_keywords

    def get_full_credits(self, 
                         isDirector=True, 
                         isWritenby=True, 
                         isCastList=True):
        
        credits_page = requests.get(self.url_fullcredits)
        if credits_page.status_code == 200:
            credits_page_soup = BeautifulSoup(credits_page.text, 'html.parser')
            credits_div = credits_page_soup.find('div', {"id": "fullcredits_content"})

            all_h4 = credits_div.find_all('h4')
            all_table = credits_div.find_all('table')
            
            if isDirector:
                table = all_table[0]
                self.director = self.get_credits_from_table(table, 'director')

            if isWritenby:
                table = all_table[1]
                self.writtenby = self.get_credits_from_table(table, 'writer')

            if isCastList:
                table = all_table[2]
                self.cast_list = self.get_credits_from_table(table, 'cast_list')
                

    def get_credits_from_table(self, table, credit_type):
        lst = []
        trs = table.find_all('tr')
        del trs[0]
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) > 1:
                if credit_type == 'cast_list':
                    td = tds[1]
                else:
                    td = tds[0]
                link = td.find('a')
                if link != None: 
                    lst.append(link.text.strip())
        return lst


    def get_cast_list(self):
        return self.cast_list[0:self.cast_list_number]

    def get_plot_keywords_list(self):
        return self.plot_keywords[0:self.plot_keywords_number]


    