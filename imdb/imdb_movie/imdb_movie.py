from bs4 import BeautifulSoup
import requests
from decimal import Decimal
from imdb.base_imdb.imdb_title import IMDBTitle

class ImdbMovie(IMDBTitle):
    def __init__(self, url=None, title=None, credit_flags = None):
        super(ImdbMovie, self).__init__(url=url, title=title)
        
        if credit_flags != None:
            self.credits_flags = credit_flags
        
        self.get_title_name()
        self.get_ratings()
        self.get_genres()
        self.get_plot_keywords()
        self.get_full_credits()


    def get_title_name(self):
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

    def get_full_credits(self):  
        credits_page = requests.get(self.url_fullcredits)
        if credits_page.status_code == 200:
            credits_page_soup = BeautifulSoup(credits_page.text, 'html.parser')
            credits_div = credits_page_soup.find('div', {"id": "fullcredits_content"})

            all_h4 = credits_div.find_all('h4')
            all_table = credits_div.find_all('table')
            
            order_dict = {}
            count = 0
            keys = self.credits_flags.keys()
            keys = list(keys)
            for h4 in all_h4:
                text = h4.text.strip()
                for key in keys:
                    if key in text:
                        order_dict[key] = count
                        keys.remove(key)
                count += 1

            if self.credits_flags['Directed']:
                table = all_table[order_dict['Directed']]
                self.director = self.get_credits_from_table(table, '')

            if self.credits_flags['Writing']:
                table = all_table[order_dict['Writing']]
                self.writtenby = self.get_credits_from_table(table, '')

            if self.credits_flags['Cast']:
                table = all_table[order_dict['Cast']]
                self.cast_list = self.get_credits_from_table(table, 'cast_list')
                

    def get_credits_from_table(self, table, credit_type):
        lst = []
        trs = table.find_all('tr')
        if credit_type == 'cast_list':
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


    def get_cast_list_top(self, top):
        if len(self.cast_list) < top:
            return self.cast_list
        return self.cast_list[0:top]

    def get_plot_keywords_list_top(self, top):
        if len(self.plot_keywords) < top:
            return self.plot_keywords
        return self.plot_keywords[0:top]


    