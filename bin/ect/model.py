from datetime import date

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean, select
from sqlalchemy.orm import declarative_base, relationship, Session

from bin.ect import cfg

ENGINE = create_engine("sqlite:///" + cfg.PATH_DB, echo=True)
BASE = declarative_base()


class Users(BASE):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    update_time = Column(Date)
    suggestions = relationship("Suggestions", backref="Users")
    feedbacks = relationship("Feedbacks", backref="Users")
    answers = relationship("Answers", backref="Users")

    @staticmethod
    def add(user_id: int, name: str) -> None:
        with Session(ENGINE) as session:
            user = Users(
                user_id=user_id,
                name=name,
                update_time=date.today()
            )
            session.add(user)
            session.commit()

    @staticmethod
    def update(user_id: int, name: str) -> None:
        with Session(ENGINE) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            user.name = name
            user.update_time = date.today()
            session.commit()

    @staticmethod
    def get(user_id: int):
        with Session(ENGINE) as session:
            return session.query(Users).filter(Users.user_id == user_id).first()


class Suggestions(BASE):
    __tablename__ = "suggestions"

    suggestion_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)

    @staticmethod
    def add(user_id: int, text: str) -> None:
        with Session(ENGINE) as session:
            suggestion = Suggestions(
                text=text,
                user_id=user_id,
                time=date.today()
            )
            session.add(suggestion)
            session.commit()

    @staticmethod
    def get(n: int = None) -> list:
        with Session(ENGINE) as session:
            query = session.query(Suggestions.user_id, Suggestions.text, Suggestions.time, Users.name.label('user_name')) \
                .join(Users).order_by(Suggestions.time.desc())
            if not n:
                return query.all()
            else:
                return query.limit(n).all()


class Feedbacks(BASE):
    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)

    @staticmethod
    def add(user_id: int, text: str) -> None:
        with Session(ENGINE) as session:
            feedback = Feedbacks(
                text=text,
                user_id=user_id,
                time=date.today()
            )
            session.add(feedback)
            session.commit()

    @staticmethod
    def get(n: int = None) -> list:
        with Session(ENGINE) as session:
            query = session.query(Feedbacks.time, Feedbacks.text, Feedbacks.user_id, Users.name.label('user_name')) \
                .join(Users).order_by(Feedbacks.time.desc())
            if not n:
                return query.all()
            else:
                return query.limit(n).all()


class Questions(BASE):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True)
    text = Column(String)
    order = Column(Integer)
    visible = Column(Boolean, default=True)
    update_time = Column(Date)
    answers = relationship("Answers", backref="Questions")

    @staticmethod
    def get(question_id: int = None, only_visible: bool = False):
        with Session(ENGINE) as session:
            query = session.query(Questions)
            if only_visible:
                query = query.filter(Questions.visible == True)
            if not question_id:
                return query.order_by(Questions.order).all()
            else:
                return query.filter(Questions.question_id == question_id).first()

    @staticmethod
    def add(text: str, order: int = 0, visible: bool = True) -> None:
        with Session(ENGINE) as session:
            question = Questions(
                text=text,
                order=order,
                visible=visible,
                update_time=date.today()
            )
            session.add(question)
            session.commit()

    @staticmethod
    def update(question_id: int, text: str = '', order: int = 0, visible: bool = True) -> None:
        with Session(ENGINE) as session:
            question = session.query(Questions).filter(Questions.question_id == question_id).first()
            if text:
                question.text = text
            if order:
                question.order = order
            question.visible = visible
            question.update_time = date.today()
            session.commit()


class Answers(BASE):
    __tablename__ = "answers"

    answer_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    text = Column(String)
    time = Column(Date)

    @staticmethod
    def add(user_id: int, answers: dict) -> None:
        with Session(ENGINE) as session:
            today = date.today()
            for id, text in answers.items():
                session.add(Answers(
                    user_id=user_id,
                    question_id=id,
                    text=text,
                    time=today
                ))
            session.commit()

    @staticmethod
    def get(n: int = None) -> list:
        columns = (
            Answers.answer_id,
            Answers.question_id,
            Answers.user_id,
            Answers.text,
            Answers.time,
            Users.name.label('user_name'),
            Questions.text.label('question_text')
        )
        with Session(ENGINE) as session:
            if not n:
                return session.query(*columns).join(Users).join(Questions).order_by(Answers.time.desc()).all()
            else:
                subquery = session.query(Answers.user_id, Answers.time).order_by(Answers.time.desc())\
                    .distinct().limit(n).subquery()
                return session.query(*columns).join(Users).join(Questions)\
                    .join(subquery, (Answers.user_id == subquery.c.user_id) & (Answers.time == subquery.c.time))\
                    .order_by(Answers.time.desc()).all()


class Columns(BASE):
    __tablename__ = "columns"

    column_id = Column(Integer, primary_key=True)
    text = Column(String)
    order = Column(Integer)
    visible = Column(Boolean, default=True)
    update_time = Column(Date)

    @staticmethod
    def add(text: str, order: int = 0, visible: bool = True) -> None:
        with Session(ENGINE) as session:
            column = Columns(
                text=text,
                order=order,
                visible=visible,
                update_time=date.today()
            )
            session.add(column)
            session.commit()

    @staticmethod
    def get(column_id: int = None):
        with Session(ENGINE) as session:
            query = session.query(Columns).order_by(Columns.order.desc())
            if column_id:
                return query.filter(Columns.column_id == column_id).first()
            else:
                return query.all()

    @staticmethod
    def update(column_id: int, text: str, order: int = 0, visible: bool = True) -> None:
        with Session(ENGINE) as session:
            column = session.query(Columns).filter(Columns.column_id == column_id).first()
            column.text = text
            column.order = order
            column.visible = visible
            column.update_time = date.today()
            session.commit()


BASE.metadata.create_all(ENGINE)
