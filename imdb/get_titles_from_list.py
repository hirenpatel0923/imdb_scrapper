from bs4 import BeautifulSoup
import requests
from imdb.base_imdb.imdb_page import IMDBPage

class IMDBList(IMDBPage):
    def __init__(self, url=None, title=None):
        super(IMDBList, self).__init__(url=url, title=title)
        self.items = 0
        self.page_count = 0
        self.page_url_list = []


        self.get_items()
        self.get_page_count()
        self.get_page_url_links()

    def get_items(self):
        self.items = self.page_soup.find(class_='desc lister-total-num-results').text.split(' ')[0]
        return self.items

    def get_page_count(self):
        self.page_count = self.items / 100
        return self.page_count

    def get_page_url_links(self):
        for i in self.page_count:
            url = 'https://www.imdb.com/list/'+ str(self.title) +'/?sort=list_order,asc&st_dt=&mode=detail&page=' + str(i + 1)
            self.page_url_list.append(url)
        return self.page_url_list