import psycopg2
from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
from . import models
from . import views
from .exceptions import (
    DuplicationException,
    InvalidEntryException
)

from relatome.validator import (
    UserQCardModelValidator,
    AuthValidator
)

class AuthController(object):
    def __init__(self):
        self.authModel = models.AuthModel(AuthValidator())
        self.authView = views.AuthView()

    def register(self, form):
        try:
            user = self.authModel.register(form)
        except InvalidEntryException as e:
            return self.authView.render_invalid_entry_exc(e)
        return self.authView.render_success()
    
    def login(self, form, session):
        print("in login begin")
        try:
            user = self.authModel.login(form)
        except InvalidEntryException as e:
            return self.authView.render_invalid_entry_exc(e)
        session['userid'] = user.id
        print("in login")
        print(user)
        return self.authView.renderuser(user)

    def logout(self, session):
        session.clear()
        return {}, 200

    def loggedInUser(self, session):
        print(session)
        userid = session.get('userid')
        return {'userid': userid} if userid else {}, 200
    

class APIController(object):
    def __init__(self):

        self.userQCardModel = models.UserQCardModel(
                UserQCardModelValidator())

        self.relStatsModel = \
            models.RelationshipStatisticsModel()

        self.questionModel = models.QuestionModel()

        self.qCardView = views.QCardView()
        self.questionView = views.QuestionView()
        self.relView = views.RelationshipView()

    def get_qcards(self, userid):
        try:
            qcards = self.userQCardModel.get_qcards(userid)
            print(list(qcards))
            return self.qCardView.renderall(qcards)
        except TypeError as err:
            print("Cannot get user data")
            return self.qCardView.render_500(err)

    def add_qcard(self, questionid, userid):
        try:
            results = self.userQCardModel.add_qcard(questionid, userid)
        except DuplicationException as e:
            return self.qCardView.render_duplication_exc(e)
        except InvalidEntryException as e:
            return self.qCardView.render_invalid_entry_exc(e)
        return self.qCardView.renderone(results)

    def delete_qcard(self, qid):
        try:
            result = self.userQCardModel.delete_qcard(qid)
        except InvalidEntryException as e:
            return self.qCardView.render_invalid_entry_exc(e)
        return self.qCardView.renderone(result)

    def get_search_results(self, q):
        results = self.questionModel.fuzzy_get(q)
        return self.questionView.renderall(results)

    def get_all_questions(self):
        results = self.questionModel.get_all()
        return self.questionView.renderall(results)

    def add_relationship(self, qid, direction, target):
        print('begin')
        try:
            result = self.userQCardModel.add_relationship(
                    qid, direction, target)
        except InvalidEntryException as e:
            print('exception')
            return self.qCardView.render_invalid_entry_exc(e)
        print('end')
        return self.qCardView.renderone(result)

    def update_relationship(self, rid, target):
        try:
            result = self.userQCardModel.update_relationship(
                    rid, target)
        except InvalidEntryException as e:
            return self.qCardView.render_invalid_entry_exc(e)
        return self.qCardView.renderone(result)

    def delete_relationship(self, rid):
        try:
            result = self.userQCardModel.delete_relationship(rid)
        except InvalidEntryException as e:
            return self.qCardView.render_invalid_entry_exc(e)
        return self.qCardView.renderone(result)

    def get_target_modes_with_direction_and_question(
            self, direction, question):
        result=self.relStatsModel.\
                get_target_modes_with_direction_and_question(
                        direction, question)
        return self.relView.render_modes(result)

    def get_target_modes_with_direction_and_questionid(
            self, direction, questionid):
        result=self.relStatsModel.\
                get_target_modes_with_direction_and_questionid(
                        direction, questionid)
        return self.relView.render_modes(result)

    def get_target_modes_with_questionid_and_all_directions(self, questionid):
        result = self.relStatsModel.\
                get_target_modes_with_questionid_and_all_directions(questionid)
        question = self.questionModel.from_id(questionid)
        return self.relView.render_question_info_view(result, question)




if __name__ == '__main__':
    pass
