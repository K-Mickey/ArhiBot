from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bin.ect import cfg

engine = create_engine("sqlite:////" + cfg.PATH_DB)
Session = sessionmaker(bind=engine)
session = Session()
