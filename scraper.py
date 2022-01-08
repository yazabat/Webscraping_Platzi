import requests
import lxml.html as html
import os

from requests.models import DEFAULT_REDIRECT_LIMIT 
import datetime

HOME_URL= 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = ' //h2[@class="headline"]/a/@href'
XPATH_BODY = '//div[@class="row article-wrapper"]//p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
        #with es un manejador contextual para que el archivo no se corrompa
            with open(f'{today}/{body}.txt','w', encoding = 'utf-8') as f:
                for p in body:
                    f.write(p)
                    f.write('\n\n')
        else:    
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response =requests.get(HOME_URL)
        #AQUI PREGUNTO
        if response.status_code==200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
        today = datetime.date.today().strftime('%d-%m-%Y')
        if not os.path.isdir(today):
            os.mkdir(today)

        for link in links_to_notices:
            parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
            
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__=='__main__':
    run()