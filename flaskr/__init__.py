import os

from flask import Flask, request

from flaskr.knowledgeBase.__init__ import Data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    try:
        data = Data()
    except:
        print('cannot load data')

    # a simple page that says hello
    @app.route('/api/ping')
    def hello():
        return 'pong'

    @app.route('/api/v1/data', methods=['GET'])
    def data():
        data = Data()
        return data.get_raw_data()

    @app.route('/api/v1/question', methods=['GET'])
    def question():
        question = request.args.get('question', default='', type=str)
        data = Data()
        answer = data.get_answers(question)

        print('\n==========>>>ANSWER on ', question)
        print(answer)

        return answer

    return app
