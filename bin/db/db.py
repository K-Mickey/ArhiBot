from datetime import date

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship, Session

from bin.ect import cfg

ENGINE = create_engine("sqlite:///" + cfg.PATH_DB, echo=True)
BASE = declarative_base()


def add_feedback(user_id: int, text: str) -> None:
    with Session(ENGINE) as session:
        feedback = Feedbacks(
            text=text,
            user_id=user_id,
            time=date.today()
        )
        session.add(feedback)
        session.commit()


def add_suggestion(user_id: int, text: str) -> None:
    with Session(ENGINE) as session:
        suggestion = Suggestions(
            text=text,
            user_id=user_id,
            time=date.today()
        )
        session.add(suggestion)
        session.commit()


def add_answers(user_id: int, answers: dict) -> None:
    with Session(ENGINE) as session:
        today = date.today()
        for id, text in answers.items():
            session.add(Answers(
                user_id=user_id,
                question_id=id,
                text=text,
                date=today
            ))
        session.commit()


def get_questions() -> list:
    with Session(ENGINE) as session:
        return session.query(Questions).filter(Questions.visible is True) \
            .sort_by(Questions.order).all()


class Users(BASE):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    update_time = Column(Date)
    suggestions = relationship("Suggestions", backref="Users")
    feedbacks = relationship("Feedbacks", backref="Users")
    answers = relationship("Answers", backref="Users")


class Suggestions(BASE):
    __tablename__ = "suggestions"

    suggestion_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)


class Feedbacks(BASE):
    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)


class Questions(BASE):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True)
    text = Column(String)
    order = Column(Integer)
    visible = Column(Boolean, default=True)
    update_time = Column(Date)
    answers = relationship("Answers", backref="Questions")


class Answers(BASE):
    __tablename__ = "answers"

    answer_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)


class Columns(BASE):
    __tablename__ = "columns"

    column_id = Column(Integer, primary_key=True)
    text = Column(String)
    order = Column(Integer)
    visible = Column(Boolean, default=True)
    update_time = Column(Date)


BASE.metadata.create_all(ENGINE)
