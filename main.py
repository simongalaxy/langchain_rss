from tools.webscraper import scrape_all_rss_links, scrape_feed_content
from tools.rssFeeder import load_rss_feed, fetch_rss_feeds
from tools.database import init_db, insert_feeds, get_all_feeds, query_columns
from tools.summarizer import TextSummarizer

from pprint import pprint
import schedule
import time


# function to summarize the content of feeds.
def summarize_feed_content(feeds: list[dict]) -> list[dict]:
    
    # init textsummarizer.
    summarizer = TextSummarizer(
        model_name="tinyllama", # llama3
        temperature=0.3,
        chunk_size=4000
        )
    
    for feed in feeds:
        if "Main content not found." in feed["Content"]:
            continue
        summary = summarizer.bullet_point_summary(feed["Content"])
        feed["AI_Summary"]=summary
        print("---------------------------------------------------------------\n")
        print(f"Summary: {summary}\n")
        print("---------------------------------------------------------------\n")
        
    return feeds


# main program.
def main():
    
    # urls for getting all rss feed links.
    urls = ["https://www.gov.hk/tc/about/rss.htm", "https://www.gov.hk/en/about/rss.htm"]
    # urls = ["https://www.gov.hk/tc/about/rss.htm"]
    
    # init database.
    init_db()

    # scrape all the rss feed links from website.
    rss_links = []
    for url in urls:
        for link in scrape_all_rss_links(url):
            rss_links.append(link)
    
    print(f"total no. of feed links: {len(rss_links)}")
    
    # fetch rss and save them to 
    all_feeds = fetch_rss_feeds(rss_links=rss_links)
    print(f"Total No. of feeds: {len(all_feeds)}")
    
    # summarize the passages in bullit point form and save it to all_feeds.
    summarized_feeds = summarize_feed_content(feeds=all_feeds)
    print("summarized feeds done.")
    
    # load all feeds into database.
    insert_feeds(data=summarized_feeds)
    print("inserted all feeds to database.")
    
    return



# program entry point.
if __name__ == "__main__":
    main()
