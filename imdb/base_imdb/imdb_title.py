from bs4 import BeautifulSoup
import requests
from imdb.base_imdb.imdb_page import IMDBPage

class IMDBTitle(IMDBPage):
    def __init__(self, url=None, title=None):
        super(IMDBTitle, self).__init__(url=url, title=title)
        
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

        


