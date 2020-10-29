from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
import abc


class View(object):

    __metaclass = abc.ABCMeta

    def render_500(self, err):
        tb = err.__traceback__
        while tb.tb_next:
            tb = tb.tb_next
        return {'error': "Error: {0}, In {1}".format(
            str(err), str(tb.tb_frame))}, 500

    def render_duplication_exc(self, err):
        return {'error': err.dic}, 403

    def render_invalid_entry_exc(self, err):
        return {'error': err.dic}, 403


class AuthView(View):
    def render_success(self):
        return {'status': 'success'}, 200

    def renderuser(self, user):
        user = user.to_dict()
        user.pop('password_hash')
        return user


class RelationshipView(View):
    def render_modes(self, res):
        if not res:
            return {}, 200
        return res.to_dict(), 200

    def render_question_info_view(self, res, question):
        return {"modes": [r.to_dict() for r in res],
                "question": question.question,
                "questionid": question.id}, 200


class QCardView(View):
    def renderone(self, qcard):
        if not qcard:
            return {}, 200
        return qcard.to_dict(), 200

    def renderall(self, qcards):
        '''
        Arguments
        qcards: iterator
        '''
        # consume generator here
        if not qcards:
            return {'qcards': []}, 200
        return {'qcards': [qcard.to_dict() for qcard in qcards]}, 200


class QuestionView(View):
    def renderone(self, question):
        if not question:
            return {}, 200
        return question.to_dict(), 200

    def renderall(self, questions):
        '''
        Arguments
        qcards: iterator
        '''
        # consume generator here
        if not questions:
            return {'questions': []}, 200
        return {'questions': [q.to_dict() for q in questions]}, 200
