# %%
#. WEB SCRAPPING CHALLANGE #daily nation #SCRAPPING HEADLINES AND SUMMERIES
import requests
from bs4 import BeautifulSoup


def news_extractor(url):
    """extract headlines and summeries from the news homepage"""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception('Failed to retrieve page: ', e)

    
    soup = BeautifulSoup(response.text, 'html.parser')
        
    headlines = []
    summaries = []
        
    for article in soup.select('article'):
        headline = article.select_one('h3')
        summary = article.select_one('p')
            
        if headline and summary:
            headlines.append(headline.text)
            summaries.append(summary.text)
    return headlines, summaries
    
        
    
if __name__=='__main__' :
    url = 'https://www.bbc.com/news'
    headlines, summaries = news_extractor(url)
        
    for i, (headline, summary) in enumerate(zip(headlines, summaries), 1):
        print(f'{i}. {headline}')
        print(f'Summary: {summary}')


