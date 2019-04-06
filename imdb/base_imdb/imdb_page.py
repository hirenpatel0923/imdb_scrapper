from bs4 import BeautifulSoup
import requests

class IMDBPage():
    def __init__(self, url=None, title=None):
        self.url = None
        self.title = None
        self.page_soup = None
        
        if url != None:
            self.url = url
            self.get_title_from_url()

        if title != None:
            self.title = title
            self.get_url_from_title()

        self.generate_page_soup()

    def get_title_from_url(self):
        self.title = self.url.split('/')[4]
        return self.title

    def get_url_from_title(self):
        if 'tt' in self.title:
            self.url = 'http://www.imdb.com/title/' + self.title
        elif 'ls' in self.title:
            self.url = 'http://www.imdb.com/list/' + self.title
        else:
            pass
        return self.url

    def generate_page_soup(self):
        if self.url != None:
            page = requests.get(self.url)
            self.page_soup = BeautifulSoup(page.text, 'html.parser')
            return True
        else:
            return False