import json
from datetime import datetime

from flask import Flask, request, make_response, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from knowledge.knowledge import KnowledgeManager

app = Flask(__name__)
Bootstrap(app)
app.config['TESTING'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knowledge/knowledge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class KnowledgeDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    countries = db.Column(db.ARRAY(db.String(1024)), nullable=False)
    answer = db.Column(db.String(64), nullable=True)
    links = db.Column(db.ARRAY(db.String(1024)), nullable=True)
    additionalAnswers = db.Column(db.ARRAY(db.String(1024)), nullable=True)
    additionalLinks = db.Column(db.ARRAY(db.String(1024)), nullable=True)
    dateCreate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.id


if __name__ == "__main__":
    app.run(debug=True)

knowledgeManager = KnowledgeManager()


@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        categories=knowledgeManager.get_categories()
    )


@app.route('/api/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/api/add', methods=['POST'])
def add():
    question = request.form['question']
    category = request.form['category']
    answer = request.form['answer']
    links = request.form['links']
    additionalAnswers = request.form['additionalAnswers']
    additionalLinks = request.form['additionalLinks']

    print('request.args', additionalLinks, additionalAnswers, links, answer, category, question)
    return redirect('/')


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
