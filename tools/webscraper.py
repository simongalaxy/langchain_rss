import requests
from bs4 import BeautifulSoup

# scrape all rssfeed links from webpage.
def scrape_all_rss_links(url: str) -> list[str]:
    
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find_all("a", attrs={"class": "contentLink"}, href=True)
    
    rss_links = []
    for item in table:
        link = item.get("href")
        if link.endswith("rss.xml") and not "www.lcsd.gov.hk" in link and not "www.edb.gov.hk" in link: # for excluding error in title from lcsd rss feeds.
           rss_links.append(link)

    return rss_links


# scrape the contenct of a rss feed.
def scrape_feed_content(news_url: str) -> str:

    response = requests.get(url=news_url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find("main")
    if article:
        content = article.get_text(separator="\n", strip=True)
    else:
        content = "Main content not found."
    
    return content

