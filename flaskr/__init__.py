import json
import os

from flask import Flask, request, make_response

from flaskr.knowledge.knowledge import Knowledge, KnowledgeManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        knowledgeBASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    knowledgeManager = KnowledgeManager()

    @app.route('/api/ping', methods=['GET'])
    def ping():
        return 'pong'

    @app.route('/api/v1/knowledge', methods=['GET'])
    def knowledge():
        return knowledgeManager.get_json_data()

    @app.route('/api/v1/knowledge/meta', methods=['GET'])
    def knowledge_meta():
        return knowledgeManager.get_json_basic_functionality()

    @app.route('/api/v1/categories', methods=['GET'])
    def get_categories():
        headers = {"Content-Type": "application/json"}

        return make_response(
            json.dumps(knowledgeManager.get_categories()),
            200,
            headers
        )

    @app.route('/api/v1/question', methods=['GET'])
    def question():
        question = request.args.get('question', default='', type=str)
        answer = knowledgeManager.get_answers(question)
        headers = {"Content-Type": "application/json"}

        return \
            make_response(
                json.dumps(answer),
                200,
                headers
            )

    return app
