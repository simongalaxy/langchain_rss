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


# Query all feeds
def get_all_feeds() -> List[RSS_Feed]:
    with Session(engine) as session:
        return session.exec(select(RSS_Feed)).all()


# Query specific columns from the database
def query_columns(columns: List[str], where_clause: Optional[Dict[str, any]] = None) -> List[tuple]:
    """
    Query specific columns from the RSS_Feed table.
    
    Args:
        columns: List of column names to query (e.g., ["id", "Title", "Feed_URL"])
        where_clause: Optional dict of column_name: value pairs for filtering
        
    Returns:
        List of tuples containing the queried column values
        
    Example:
        results = query_columns(
            columns=["Title", "Feed_URL"],
            where_clause={"Category": "Tech"}
        )
    """
    with Session(engine) as session:
        # Build the column selection
        column_attrs = [getattr(RSS_Feed, col) for col in columns]
        
        # Create the select statement
        statement = select(*column_attrs)
        
        # Add where conditions if provided
        if where_clause:
            for col_name, value in where_clause.items():
                statement = statement.where(getattr(RSS_Feed, col_name) == value)
        
        # Execute and return results
        results = session.exec(statement).all()
        
        return results
