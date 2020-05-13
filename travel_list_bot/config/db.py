from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from travel_list_bot.models import Base, Place, Chat


db_engine = create_engine('sqlite:///db.sqlite3', echo=False)
Session = sessionmaker(bind=db_engine)
Base.metadata.create_all(db_engine)
session = scoped_session(sessionmaker(bind=db_engine))
