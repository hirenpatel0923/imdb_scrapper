from bs4 import BeautifulSoup
import requests

class IMDBTitle():
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
        
        self.title_name = ''
        self.ratings = 0.0
        self.genres = []
        self.plot_keywords = []
        self.url_fullcredits = 'https://www.imdb.com/title/' + self.title + '/fullcredits'
        self.director = []
        self.writtenby = []
        self.cast_list = []
        self.credits_flags = {'Directed': False,
                              'Writing': False,
                              'Cast': False,
                              'Produced': False,
                              'Music': False,
                              'Cinematography': False,
                              'Film': False,
                              'Art': False,
                              'Makeup': False,
                              'Production': False,
                              'Sound': False,
                              'Camera': False,
                              }

        self.generate_page_soup()


    def get_title_from_url(self):
        self.title = self.url.split('/')[4]
        return self.title

    def get_url_from_title(self):
        self.url = 'http://www.imdb.com/title/' + self.title
        return self.url

    def generate_page_soup(self):
        if self.url != None:
            page = requests.get(self.url)
            self.page_soup = BeautifulSoup(page.text, 'html.parser')
            return True
        else:
            return False