import json

from fuzzywuzzy import fuzz

from project import db
from project.api.models import LogsManager
from project.tables import KnowledgeSchema, UnansweredQuestions


class KnowledgeManager:
    def __init__(self):
        self.knowledgeDAL = KnowledgeDAL()
        self.logManager = LogsManager()

    def get_meta_all_data(self):
        # self.logManager.add_log(
        #     type='GET',
        #     message='Getting all meta',
        #     info='get_meta_all_data',
        # )

        all_meta = self.knowledgeDAL.get_meta_all_data()

        # self.logManager.add_log(
        #     type='GOT',
        #     message='GOT',
        #     info='get_meta_all_data',
        # )

        return all_meta

    def get_meta_categories(self):
        # self.logManager.add_log(
        #     type='GET',
        #     message='Getting categories',
        #     info='get_meta_categories',
        # )

        categories = self.knowledgeDAL.get_meta_categories()

        # self.logManager.add_log(
        #     type='GOT',
        #     message='GOT',
        #     info='get_meta_categories',
        # )

        return categories

    def get_all_data(self):
        # self.logManager.add_log(
        #     type='GET',
        #     message='Getting all data',
        #     info='get_all_data',
        # )

        results_all_dal = self.knowledgeDAL.get_all_data()
        results_dto = []

        for result_dal in results_all_dal:
            knowledgeDto = {}

            knowledgeDto['id'] = result_dal.__dict__['id']
            knowledgeDto['question'] = result_dal.__dict__['question']
            knowledgeDto['category'] = result_dal.__dict__['category']
            knowledgeDto['answer'] = result_dal.__dict__['answer']
            knowledgeDto['links'] = result_dal.__dict__['links']
            knowledgeDto['countries'] = result_dal.__dict__['countries']
            knowledgeDto['additional_answers'] = result_dal.__dict__['additional_answers']
            knowledgeDto['additional_links'] = result_dal.__dict__['additional_links']
            knowledgeDto['date_created'] = result_dal.__dict__['date_created'].strftime(
                "%m/%d/%y %H:%M:%S")

            results_dto.insert(0, knowledgeDto)

        # self.logManager.add_log(
        #     type='GOT',
        #     message='Getting all data.',
        #     info='get_all_data',
        # )

        return results_dto

    def get_knowledge(self, id):
        knowledge_dal = self.knowledgeDAL.get_knowledge(id)
        knowledge_dto = {}

        knowledge_dto['id'] = knowledge_dal.__dict__['id']
        knowledge_dto['question'] = knowledge_dal.__dict__['question']
        knowledge_dto['category'] = knowledge_dal.__dict__['category']
        knowledge_dto['answer'] = knowledge_dal.__dict__['answer']
        knowledge_dto['links'] = knowledge_dal.__dict__['links']
        knowledge_dto['countries'] = knowledge_dal.__dict__['countries']
        knowledge_dto['additional_answers'] = knowledge_dal.__dict__['additional_answers']
        knowledge_dto['additional_links'] = knowledge_dal.__dict__['additional_links']

        return knowledge_dto

    def get_answers(self, question):
        # self.logManager.add_log(
        #     type='[GET] Answer',
        #     message=f'Getting answer for {question} question',
        #     info='get_answers'
        # )

        results_all_dal = self.knowledgeDAL.get_all_data()
        results_dto = []

        for result_dal in results_all_dal:
            if fuzz.token_set_ratio(result_dal.__dict__['question'], question) > 95:
                knowledgeDto = {}

                knowledgeDto['id'] = result_dal.__dict__['id']
                knowledgeDto['question'] = result_dal.__dict__['question']
                knowledgeDto['category'] = result_dal.__dict__['category']
                knowledgeDto['answer'] = result_dal.__dict__['answer']
                knowledgeDto['links'] = result_dal.__dict__['links']
                knowledgeDto['countries'] = result_dal.__dict__['countries']
                knowledgeDto['additional_answers'] = result_dal.__dict__['additional_answers']
                knowledgeDto['additional_links'] = result_dal.__dict__['additional_links']
                results_dto.insert(0, knowledgeDto)

        # self.logManager.add_log(
        #     type='[GOT] Answer',
        #     message=f'Got answer for {question} question. Answer ${json.dumps(results_dto)}',
        #     info='get_answers'
        # )

        return results_dto

    def add_knowledge(self,
                      question,
                      category,
                      answer,
                      countries,
                      links,
                      additional_answers,
                      additional_links,
                      ):
        return self.knowledgeDAL.add_knowlegde(
            question=question,
            category=category,
            answer=answer,
            countries=countries,
            links=links,
            additional_answers=additional_answers,
            additional_links=additional_links,
        )

    def delete_knowledge(self, id):
        return self.knowledgeDAL.delete_knowledge(id)

    def update_knowledge(self,
                         id,
                         question,
                         category,
                         answer,
                         countries,
                         links,
                         additional_answers,
                         additional_links,
                         ):
        return self.knowledgeDAL.update_knowledge(
            id=id,
            question=question,
            category=category,
            answer=answer,
            countries=countries,
            links=links,
            additional_answers=additional_answers,
            additional_links=additional_links,
        )


class KnowledgeDAL:
    def __init__(self):
        with open('project/db/knowledge_metadata.json') as f:
            self.knowledgeMetaJsonData = json.load(f)

    def get_meta_all_data(self):
        return self.knowledgeMetaJsonData

    def get_meta_categories(self):
        return self.knowledgeMetaJsonData['categories']

    def get_all_data(self):
        return db.session.query(KnowledgeSchema).order_by(KnowledgeSchema.date_created).all()

    def get_knowledge(self, id):
        return db.session.query(KnowledgeSchema).get_or_404(id)

    def add_knowlegde(self,
                      question,
                      category,
                      answer,
                      countries,
                      links,
                      additional_answers,
                      additional_links,
                      ):
        new_knowledge = KnowledgeSchema(
            question=question,
            category=category,
            answer=answer,
            countries=countries,
            links=links,
            additional_answers=additional_answers,
            additional_links=additional_links,
        )

        try:
            db.session.add(new_knowledge)
            db.session.commit()
            return 'Success'
        except Exception as e:
            raise Exception('Error e'.format(e))

    def delete_knowledge(self, id):
        knowledge_to_delete = db.session.query(KnowledgeSchema).get_or_404(id)

        try:
            db.session.delete(knowledge_to_delete)
            return db.session.commit()
        except:
            raise Exception(f'Cannot delete knowledge with id ${id} from db')

    def update_knowledge(self,
                         id,
                         question,
                         category,
                         answer,
                         countries,
                         links,
                         additional_answers,
                         additional_links,
                         ):
        try:
            knowledge_to_update = db.session.query(KnowledgeSchema).get_or_404(id)
            knowledge_to_update.question = question
            knowledge_to_update.category = category
            knowledge_to_update.answer = answer
            knowledge_to_update.countries = countries
            knowledge_to_update.links = links
            knowledge_to_update.additional_answers = additional_answers
            knowledge_to_update.additional_links = additional_links

            try:
                return db.session.commit()
            except Exception as e:
                print('Commiting error. ' + str(e))
                raise Exception(f'Cannot update knowledge with id ${id} from db')
        except Exception as e:  # work on python 3.x
            print('Retrieving error. ' + str(e))


class UnAnsweredManager:
    def delete_unanswered(self, id):
        unanswered_to_delete = db.session.query(UnansweredQuestions).get_or_404(id)

        try:
            db.session.delete(unanswered_to_delete)
            db.session.commit()
            return 'Success'
        except:
            print('Deleting error. ' + str(e))
            raise Exception(f'Cannot delete knowledge with id ${id} from db')

    def get_unanswered(self):
        results_all_dal = db.session.query(UnansweredQuestions).order_by(UnansweredQuestions.asked).all()
        results_dto = []

        for result_dal in results_all_dal:
            result_dto = {}

            result_dto['id'] = result_dal.__dict__['id']
            result_dto['question'] = result_dal.__dict__['question']
            result_dto['asked'] = result_dal.__dict__['asked']
            results_dto.insert(0, result_dto)

        return results_dto

    def set_unaswered(self, question):
        try:
            unanswered_all = self.get_unanswered()
            unanswered_question = next((x for x in unanswered_all if x['question'] == question), [])

            if not unanswered_all or not unanswered_question or unanswered_question is None:
                unanswered_question = UnansweredQuestions(question=question, asked=1)

                try:
                    db.session.add(unanswered_question)
                    db.session.commit()
                    return 'Success'
                except Exception as e:
                    print(f'Commit error {e}')
            else:
                db_unanswered_question = db.session.query(UnansweredQuestions).get(unanswered_question['id'])
                db_unanswered_question.asked = unanswered_question['asked'] + 1

                try:
                    db.session.commit()
                    return 'Success'
                except Exception as e:
                    print('Commiting error. ' + str(e))
                    raise Exception(f'Cannot update knowledge with id ${id} from db')

        except Exception as e:
            # raise e
            print(f'Create error. ' + str(e))
