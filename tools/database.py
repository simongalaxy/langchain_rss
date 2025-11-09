from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, create_engine, Session, select


# Define the data model
class RSS_Feed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    Category: str
    Title: str
    Publish_Date: str
    Feed_URL: str = Field(unique=True) # 👈 Enforce uniqueness
    Summary: Optional[str] = Field(default=None)
    Content: Optional[str] = Field(default=None)
    AI_Summary: Optional[str] = Field(default=None)


# Create the SQLite engine and initialize the database
engine = create_engine("sqlite:///rss_feeds.db")


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    return None

# Insert a list of dictionaries into the database
def insert_feeds(data: List[Dict]) -> None:
    with Session(engine) as session:
        for item in data:
            # Check if link already exists
            exists = session.exec(select(RSS_Feed).where(RSS_Feed.Feed_URL == item["Feed_URL"])).first()
            if not exists:
                feed = RSS_Feed(**item)
                session.add(feed)
        session.commit()

    return


# 4. Optional: Query all feeds
def get_all_feeds() -> List[RSS_Feed]:
    with Session(engine) as session:
        return session.exec(select(RSS_Feed)).all()
