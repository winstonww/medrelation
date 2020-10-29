import abc
import relatome.orm.qcardTable as qct
import relatome.orm.relationshipTable as rt
import relatome.orm.questionTable as qnt
import relatome.orm.userTable as usert
import relatome.constants as const
from flask import current_app
from pathlib import Path
from .db import get_db
from .utils import quote, clean
from fuzzywuzzy import process
from .exceptions import (
    DuplicationException,
    InvalidEntryException
)
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class AuthModel(object):
    def __init__(self, validator):
        self.validator = validator

    def register(self, form):
        self.validator.validate_register(form)
        return usert.insert(
            form['username'],
            form['email'],
            generate_password_hash(form['password'])
        )

    def login(self, form):
        self.validator.validate_login(form)
        return usert.from_username(
            form['username'])


class UserQCardModel(object):
    def __init__(self, validator):
        self.validator = validator

    def get_qcards(self, userid):
        self.validator.validate_get_qcards(userid)
        # get generator for all cards
        return qct.from_userid(userid)

    def get_qcard(self, qid):
        return qct.from_id(qid)

    def add_relationship(self, qid, direction, target):
        self.validator.validate_add_relationship(direction, target)
        qcard = qct.from_id(qid)
        rt.insert(direction, target, qid, qcard.questionid)
        return self.get_qcard(qid)

    def update_relationship(self, rid, target):
        self.validator.validate_update_relationship(target)
        return qct.from_id(rt.update(rid, target).id)

    def delete_relationship(self, rid):
        self.validator.validate_delete_relationship(rid)
        return qct.from_id(rt.delete(rid).id)

    def add_qcard(self, questionid, userid):
        '''
            Add qcard with input question to database
            @return qcard being added
        '''
        conn, db = get_db()
        # id, question, relationship_id = 0, 'Heart'
        self.validator.validate_add_qcard(questionid, userid)
        res = qct.insert(questionid, userid)
        print("in add_qcard")
        print(res)
        return res

    def delete_qcard(self, qid):
        self.validator.validate_delete_qcard(qid)
        rt.delete_with_qid(qid)
        return qct.delete(qid)

class RelationshipStatisticsModel(object):
    def get_target_modes_with_direction_and_question(
            self, direction, question):
        # self.validator.validate_get_target_modes_with_direction_and_quetion(direction, qid)
        question = qnt.from_question(question)
        return rt.get_target_modes_with_direction_and_questionid(
                direction, question.id)

    def get_target_modes_with_direction_and_questionid(
            self, direction, questionid):
        # self.validator.validate_get_target_modes_with_direction_and_questionid(direction, qid)
        return rt.get_target_modes_with_direction_and_questionid(
                direction, questionid)

    def get_target_modes_with_questionid_and_all_directions(self, questionid):
        # self.validator.validate_get_direction_modes(direction, qid)
        res = []
        for direction in rt.get_directions_with_questionid(questionid):
            res.append(
                rt.get_target_modes_with_direction_and_questionid(
                    direction, questionid)
            )
        return res


class QuestionModel(object):
    '''
        Model returns Question or list of Question
    '''

    def get_all(self):
        return qnt.all()

    def fuzzy_get(self, pattern):
        all_questions = (q.question for q in qnt.all())
        questions = process.extract(
                clean(pattern), all_questions, limit=10)
        questions.sort(key=lambda e: -e[1])
        questions = (q[0] for q in questions if q[1] > 0.7)
        return [qnt.from_question(question)
                for question in questions if questions]

    def from_id(self, questionid):
        # self.validator.validate_from_id(questionid)
        return qnt.from_id(questionid)
