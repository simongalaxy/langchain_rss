from tools.webscraper import scrape_all_rss_links, scrape_feed_content
from tools.rssFeeder import load_rss_feed
from tools.database import init_db, insert_feeds, get_all_feeds

from pprint import pprint

# main program.
def main():
    
    # init database.
    init_db()

    # scrape all the rss feed links from website.
    urls = ["https://www.gov.hk/tc/about/rss.htm", "https://www.gov.hk/en/about/rss.htm"]
    #urls = ["https://www.gov.hk/en/about/rss.htm"]

    for url in urls:
        # scrape the rss feeds link from web in url.
        rss_feeds = scrape_all_rss_links(url)

        # get title, category, publish date and link of all the passages from rss feed.
        for rss in rss_feeds:
            feeds = load_rss_feed(link=rss)
            print(f"Total feeds per rss - {rss}: {len(feeds)}")
            
            # scrape all the passage contents.
            for feed in feeds:
                content = scrape_feed_content(news_url=feed["Feed_URL"])
                feed["Content"]=content
            
            # insert feeds into sqlite database.
            insert_feeds(data=feeds)  




    return



# program entry point.
if __name__ == "__main__":
    main()
