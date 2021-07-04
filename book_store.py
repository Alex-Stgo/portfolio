import requests as req
from bs4 import BeautifulSoup as bs

class webscrap():
    def __init__(self):
        self.url = 'http://books.toscrape.com/'
        self.ratings = {'One':'1 out of 5','Two':'2 out of 5','Three':'3 out of 5','Four':'4 out of 5','Five':'5 out of 5'}
        r=req.get(self.url)
        soup=bs(r.content,"html.parser")
        nav = soup.find('ul',{'class':'nav-list'}).find('ul').find_all('li')
        self.categories={li.text.strip():li.find('a')['href'] for li in nav}
        self.titles={}
    def _get_titles(self,url):
        r=req.get(url)
        soup=bs(r.content,"html.parser")
        books=soup.find('ol').find_all('li')
        t = {book.find('h3').find('a')['title']:self.url + 'catalogue/' + book.find('a')['href'].replace("../","") for book in books if not (book.find('i',{'class':'icon-ok'}) is None)}
        self.titles.update(t)
        return soup
    def search(self):
        soup=self._get_titles(self.url + 'index.html')

        while soup.find('li',{'class':'next'}):
            href = soup.find('li',{'class':'next'}).find('a')['href']
            if not 'catalogue' in href:
                url = self.url + 'catalogue/' + href
            else:
                url = self.url + href
            soup=self._get_titles(url)
    def books_by_cat(self,cat):
        href = self.categories[cat]
        href_root = "/".join(href.split("/")[:-1])+"/"
        soup=self._get_titles(self.url + href)

        while soup.find('li',{'class':'next'}):
            href = soup.find('li',{'class':'next'}).find('a')['href']
            soup=self._get_titles(self.url + href_root + href)
        return self.titles
    def book_info(self,title):
        if self.titles=={}:
            return {}
        else:
            info={}
            if title in self.titles:
                url = self.titles[title]
                r=req.get(url)
                soup=bs(r.content,"html.parser")
                
                info['Title'] =title
                info['URL'] =url
                info['Price'] = soup.find('p',{'class':'price_color'}).text
                info['InStock'] = soup.find('p',{'class':'instock availability'}).text
                info['Rating'] = self.ratings[soup.find('p',{'class':'star-rating'})['class'][1]]
                return info
            else:
                return {}