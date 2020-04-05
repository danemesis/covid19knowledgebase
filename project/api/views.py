import json

from flask import request, Blueprint, send_file, make_response

from project.dbmanager.forms import KnowledgeForm
from project.dbmanager.models import KnowledgeManager, LogsManager, UnAnsweredManager

api_v1_blueprint = Blueprint(
    'api_v1',
    __name__,
)

knowledgeManager = KnowledgeManager()
logsManager = LogsManager()
unAnsweredManager = UnAnsweredManager()

json_headers = {"Content-Type": "application/json"}


@api_v1_blueprint.route('/db', methods=['GET'])
def api_get_db():
    return send_file('project/db/knowledge.db')


@api_v1_blueprint.route('/add', methods=['POST'])
def api_add():
    add_form = KnowledgeForm(request.form)
    if add_form.validate():
        try:
            knowledgeManager.add_knowledge(
                question=request.form['question'],
                category=request.form['category'],
                answer=request.form['answer'],
                countries=request.form['countries'],
                links=request.form['links'],
                additional_answers=request.form['additional_answers'],
                additional_links=request.form['additional_links'],
            )
            return make_response(
                json.dumps(request.form),
                200,
                json_headers
            )
        except:
            return 'There was an adding problem.'
    else:
        return 'Form data is not valid'


@api_v1_blueprint.route('/knowledge', methods=['GET'])
def api_knowledge():
    return make_response(
        json.dumps(knowledgeManager.get_all_data()),
        200,
        json_headers
    )


@api_v1_blueprint.route('/unanswered', methods=['GET'])
def api_unanswered():
    return make_response(
        json.dumps(unAnsweredManager.get_unanswered()),
        200,
        json_headers
    )


@api_v1_blueprint.route('/unanswered/<int:id>', methods=['DELETE'])
def api_delete_unanswered(id):
    return make_response(
        json.dumps(unAnsweredManager.delete_unanswered(id=id)),
        200,
        json_headers
    )


@api_v1_blueprint.route('/question', methods=['GET'])
def api_question():
    question = request.args.get('question', default='', type=str)
    answers = knowledgeManager.get_answers(question)

    if not answers:
        unAnsweredManager.set_unaswered(question)

    return make_response(
        json.dumps(answers),
        200,
        json_headers
    )


@api_v1_blueprint.route('/meta/all', methods=['GET'])
def api_get_all_meta():
    return json.dumps(knowledgeManager.get_meta_all_data())


@api_v1_blueprint.route('/meta/categories', methods=['GET'])
def api_get_categories():
    return make_response(
        json.dumps(knowledgeManager.get_meta_categories()),
        200,
        json_headers
    )


@api_v1_blueprint.route('/ping', methods=['GET'])
def api_ping():
    return 'pong from api v1'


@api_v1_blueprint.route('/logs', methods=['GET'])
def api_logs():
    return make_response(
        json.dumps(logsManager.get_all()),
        200,
        {"Content-Type": "application/json"}
    )
