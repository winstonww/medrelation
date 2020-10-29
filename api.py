import json
from flask import (
    Blueprint, flash, g, current_app, redirect, request, session, url_for
)

from .controllers import APIController

bp = Blueprint('api', __name__, url_prefix='/api')
controller = APIController()

@bp.route('/', methods=['GET'])
def test():
    return 'Hello World!'

@bp.route('/qcards', methods=['GET'])
def get_qcards():
    print("in api get_qcards")
    print(session)
    res, status = controller.get_qcards(session.get('userid'))
    print(res)
    return res, status

@bp.route('/search/<string:title>', methods=['GET'])
def get_search_results(title):
    print("in get_search_results")
    return controller.get_search_results(title)

@bp.route('/search/all', methods=['GET'])
def get_all_questions():
    print("in get_all_questions")
    return controller.get_all_questions()

@bp.route('/qcard/add', methods=['POST'])
def add_qcard():
    print("in add_qcard")
    data = json.loads(str(request.data, encoding='utf-8'))
    print(data)
    res =  controller.add_qcard(data.get("questionid"), session.get('userid'))
    print("in 35")
    print(res)
    return res

@bp.route('/qcard/<int:qid>/delete', methods=['POST'])
def delete_qcard(qid):
    print("in delete qcard")
    return controller.delete_qcard(qid)


@bp.route('/qcard/<int:qid>/relationship/add', methods=['POST'])
def add_relationship(qid):
    print("in add_relationship")
    data = json.loads(str(request.data, encoding='utf-8'))
    print(data)
    return controller.add_relationship(
            qid, data.get('direction'), data.get('target'))

@bp.route('/relationship/<int:rid>/update', methods=['POST'])
def update_relationship(rid):
    print("in update_relationship")
    data = json.loads(str(request.data, encoding='utf-8'))
    print(data)
    return controller.update_relationship(
            rid, data.get('target'))

@bp.route('/relationship/<int:rid>/delete', methods=['POST'])
def delete_relationship(rid):
    print("in delete_relationship")
    return controller.delete_relationship(rid)

@bp.route('/stats/questionid/<int:questionid>/target-modes', methods=['GET'])
def get_target_modes_with_questionid_and_all_directions(questionid):
    print("in get_target_modes_with_questionid_and_all_directions")
    return controller.\
            get_target_modes_with_questionid_and_all_directions(questionid)
