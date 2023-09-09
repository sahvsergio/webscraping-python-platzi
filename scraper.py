#import the libraries
import os#used to create folders 
import datetime
import requests
import lxml.html as html# used so that we write xpath directly in the code


#Initial url  to visit
HOME_URL=''

#assing the xpaths to a variable
XPATH_LINK_TO_ARTICLE='//h2[@class="headline"]/a/@href' 

def parse_news(link, today):
    try:
        response=requests.get(link)
        if response.status_code==200:
            news=response.content.decode('utf-8')
            parsed=html.fromstring(news)
            try:
                title=parsed.xpath(XPATH_LINK_TO_ARTICLE)[0]#title
                title=title.replace('\"','')
                summary=parsed.xpath(XPATH_LINK_TO_ARTICLE)[0]#summary of the news
                
                
            except IndexError:
                return
            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in  body:
                    f.write(p)
                    f.write('/n')
        else:
            raise ValueError(f'{response.status_code}')
    except ValueError as ve:
        print(ve)
        

def parse_home():
    try:
        response= requests.get(HOME_URL)
        if response.status_code==200:
            home= response.content.decode('utf-8')
            parsed=html.fromstring(home)
            links_to_news=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_news)
            today=datetime.date.today().strftime(' %d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
                for link in links_to_news:
                    parse_news(link, today)
        else:
            raise ValueError(f'{response.status_code}')
    except ValueError as ve:
        print(ve)
def run():
    parse_home()


if __name__=='__main__':
    run()
