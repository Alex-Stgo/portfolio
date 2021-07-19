import requests as req
from bs4 import BeautifulSoup as bs
import json
import pandas as pd


url = "https://www.jobbank.gc.ca/core/ta-jobtitle_en/select?q=data&wt=json&rows=30"
r=req.get(url)
soup=bs(r.content,"html.parser")
res=json.loads(soup.text)
jobs = [(job['noc_job_title_concordance_id'],job['noc_code'],job['title']) for job in res['response']['docs']]
print()

url = "https://www.jobbank.gc.ca/core/ta-cityprovsuggest_en/select?q=BC&fq=NOT postalcode_cnt:0&wt=json&rows=25"
r=req.get(url)
soup=bs(r.content,"html.parser")
res=json.loads(soup.text)
provinces = [(p['city_id'],p['name'],p['province_cd']) for p in res['response']['docs'] if p['city_id']!='0']
print()

data=pd.DataFrame()
for id,noc_code,job in jobs:
    for i,(city_id,city,province) in enumerate(provinces):
        i=str(i)
        url=f'https://www.jobbank.gc.ca/marketreport/wages-occupation/{id}/{city_id}'
        r=req.get(url)
        soup=bs(r.content,"html.parser")
        wage = soup.find('table',{'id':'wage-occ-report-loc'}).find('tbody').find('tr').find_all('td')
        data.loc[id+i,'Province'] = province
        data.loc[id+i,'City'] = city
        data.loc[id+i,'job'] = job
        data.loc[id+i,'NOC'] = noc_code
        data.loc[id+i,'low'] = wage[0].text.strip()
        data.loc[id+i,'median'] = wage[1].text.strip()
        data.loc[id+i,    'high'] = wage[2].text.strip()
print()






URL = "https://www.jobbank.gc.ca/career-planning/search-job-profile"
head={
'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'es-MX,es;q=0.5',
'Cache-Control':'no-cache',
'Connection':'Keep-Alive',
'Content-Length':'260',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'www.jobbank.gc.ca',
'Referer':'https://www.jobbank.gc.ca/trend-analysis/search-occupations',
'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Cookie':'__utmc=20577571; __utmz=20577571.1625609066.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=20577571.190329239.1625609066.1625609066.1625609066.1; __utmb=20577571.12.9.1625610112945; __utmt=1; JSESSIONID=32B5F94AFA96DC7AAA074960A2A43824.jobsearch74; oam.Flash.RENDERMAP.TOKEN=ns00nzadq'
}

r=req.post(URL,headers=head)
# codHTML=r.content.decode("latin1","ignore")
soup=bs(r.content,"html.parser")
print()


















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