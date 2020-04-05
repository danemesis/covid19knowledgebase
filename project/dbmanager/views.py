from flask import request, redirect, render_template, Blueprint, url_for, flash

from project.dbmanager.forms import KnowledgeForm
from project.dbmanager.models import KnowledgeManager

dbmanager_blueprint = Blueprint(
    'dbmanager',
    __name__,
    template_folder='templates'
)

knowledgeManager = KnowledgeManager()


@dbmanager_blueprint.route('/')
def index():
    all_data = knowledgeManager.get_all_data()
    categories = knowledgeManager.get_meta_categories()
    knowledge_form = KnowledgeForm()

    return render_template(
        'dbmanager/index.html',
        **locals()
    )


@dbmanager_blueprint.route('/add', methods=['POST'])
def add():
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
            flash('Knowledge added!')
            return redirect(url_for('dbmanager.index'))
        except:
            return 'There was an adding problem.'
    else:
        return 'Form data is not valid'


@dbmanager_blueprint.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    try:
        knowledgeManager.delete_knowledge(id)
        flash('Knowledge deleted!')
        return redirect(url_for('dbmanager.index'))
    except:
        return 'There was a problem with deleting.'


@dbmanager_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    categories = knowledgeManager.get_meta_categories()
    knowledge = knowledgeManager.get_knowledge(id)
    knowledge_form = KnowledgeForm()

    if request.method == 'POST':
        if KnowledgeForm(request.form).validate():
            try:
                knowledgeManager.update_knowledge(
                    id=id,
                    question=request.form['question'],
                    category=request.form['category'],
                    answer=request.form['answer'],
                    countries=request.form['countries'],
                    links=request.form['links'],
                    additional_answers=request.form['additional_answers'],
                    additional_links=request.form['additional_links'],
                )
                flash('Knowledge updated!')
                return redirect(url_for('dbmanager.index'))
            except Exception as e:
                print('There was an updating problem. Error: ' + str(e))
                return render_template('dbmanager/update.html', knowledge=knowledge, categories=categories,
                                       knowledge_form=knowledge_form, message='There was an updating problem')
        else:
            return render_template('dbmanager/update.html', knowledge=knowledge, categories=categories,
                                   knowledge_form=knowledge_form, message='Form is not valid')
    else:
        return render_template('dbmanager/update.html', knowledge=knowledge, categories=categories,
                               knowledge_form=knowledge_form)
