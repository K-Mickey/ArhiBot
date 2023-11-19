from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from bin.ect import cfg

engine = create_engine("sqlite:////" + cfg.PATH_DB)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    update_time = Column(Date)
    suggestions = relationship("Suggestions", backref="Users")
    feedbacks = relationship("Feedbacks", backref="Users")
    answers = relationship("Answers", backref="Users")


class Suggestions(Base):
    __tablename__ = "suggestions"

    suggestion_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)


class Feedbacks(Base):
    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)


class Questions(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True)
    text = Column(String)
    order = Column(Integer)
    visible = Column(Boolean, default=True)
    update_time = Column(Date)
    answers = relationship("Answers", backref="Questions")


class Answers(Base):
    __tablename__ = "answers"

    answer_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)


class Columns(Base):
    __tablename__ = "columns"

    column_id = Column(Integer, primary_key=True)
    text = Column(String)
    order = Column(Integer)
    visible = Column(Boolean, default=True)
    update_time = Column(Date)


Base.metadata.create_all(engine)
