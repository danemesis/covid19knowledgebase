from flask_wtf import FlaskForm
from wtforms import StringField, validators


class KnowledgeForm(FlaskForm):
    question = StringField('question', [validators.DataRequired()])
    category = StringField('category', [validators.DataRequired()])
    answer = StringField('answer')
    countries = StringField('countries')
    links = StringField('links')
    additional_answers = StringField('additional_answers')
    additional_links = StringField('additional_links')


class DeleteFrom(FlaskForm):
    pass
