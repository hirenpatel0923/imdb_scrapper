from bs4 import BeautifulSoup
import requests
from imdb.base_imdb.imdb_page import IMDBPage

class IMDBPageTitle(IMDBPage):
    def __init__(self, url, title):
        super(IMDBPageTitle, self).__init__(url=url, title=title)

        self.title_list = []

        self.get_title_list()

    def get_title_list(self):
        all_links = self.page_soup.find_all('a', href=True)
        for link in all_links:
            if '/title/' in link['href']:
                split_link = link['href'].split('/')
                if split_link[2] not in self.title_list:
                    self.title_list.append(split_link[2])
        return self.title_list
            