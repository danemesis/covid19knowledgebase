import json

from flask import Flask, request, make_response, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from knowledge.knowledge import KnowledgeManager, LogsManager
from knowledge.tables import Base

app = Flask(__name__)
Bootstrap(app)

app.config['TESTING'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knowledge/knowledge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['BOOTSTRAP_USE_MINIFIED'] = False

db = SQLAlchemy(app)
# db.register_base(Base)

if __name__ == "__main__":
    app.run(debug=True)

knowledgeManager = KnowledgeManager(db)
logsManager = LogsManager(db)


@app.before_first_request
def setup():
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)


@app.route('/', methods=['GET'])
def index():
    # all_data = KnowledgeDb.query.order_by(KnowledgeDb.dateCreated).all()
    # categories = knowledgeManager.get_categories()

    return render_template(
        'index.html',
        **locals()
    )


@app.route('/api/v1/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/api/v1/logs', methods=['GET'])
def logs():
    logs = logsManager.get_all()
    print('LOGS', str(logs))
    return logs


@app.route('/api/v1/add', methods=['POST'])
def add():
    question = request.form['question']
    category = request.form['category']
    answer = request.form['answer']
    countries = request.formm['countries']
    links = request.form['links']
    additionalAnswers = request.form['additionalAnswers']
    additionalLinks = request.form['additionalLinks']

    new_knowledge = KnowledgeDb(
        question=question,
        category=category,
        answer=answer,
        countries=countries,
        links=links,
        additionalAnswers=additionalAnswers,
        additionalLinks=additionalLinks,
    )

    try:
        db.session.add(new_knowledge)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem.'


@app.route('/api/v1/knowledge', methods=['GET'])
def knowledge():
    return json.dumps(knowledgeManager.get_all_data())


@app.route('/api/v1/knowledge/meta', methods=['GET'])
def knowledge_meta():
    return json.dumps(knowledgeManager.get_meta_all_data())


@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    headers = {"Content-Type": "application/json"}

    return make_response(
        json.dumps(knowledgeManager.get_meta_categories()),
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
