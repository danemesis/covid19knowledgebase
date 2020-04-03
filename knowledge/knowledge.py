import json

from fuzzywuzzy import fuzz

from knowledge.logs import LogsManager
from knowledge.tables import KnowledgeSchema


class KnowledgeManager:
    def __init__(self, db):
        self.knowledgeDAL = KnowledgeDAL(db)
        self.logManager = LogsManager(db)
        self.db = db

    def get_meta_all_data(self):
        self.logManager.add_log(
            type='GET',
            message='Getting all meta',
            info='get_meta_all_data',
        )

        all_meta = self.knowledgeDAL.get_meta_all_data()

        self.logManager.add_log(
            type='GOT',
            message='GOT',
            info='get_meta_all_data',
        )

        return all_meta

    def get_meta_categories(self):
        self.logManager.add_log(
            type='GET',
            message='Getting categories',
            info='get_meta_categories',
        )

        categories = self.knowledgeDAL.get_meta_categories()

        self.logManager.add_log(
            type='GOT',
            message='GOT',
            info='get_meta_categories',
        )

        return categories

    def get_all_data(self):
        self.logManager.add_log(
            type='GET',
            message='Getting all data',
            info='get_all_data',
        )

        results_dal = self.knowledgeDAL.get_all_data()
        results_dto = []

        for result_dal in results_dal:
            knowledgeDto = {}

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

        self.logManager.add_log(
            type='GOT',
            message='Getting all data.',
            info='get_all_data',
        )

        return results_dto

    def get_answers(self, question):
        self.logManager.add_log(
            type='[GET] Answer',
            message=f'Getting answer for {question} question',
            info='get_answers'
        )

        results_all_dal = self.knowledgeDAL.get_all_data()
        results_dto = []

        for result_data in results_all_dal:
            if fuzz.token_set_ratio(result_data.__dict__['question'], question) > 95:
                knowledgeDto = {}

                knowledgeDto['question'] = result_data.__dict__['question']
                knowledgeDto['category'] = result_data.__dict__['category']
                knowledgeDto['answer'] = result_data.__dict__['answer']
                knowledgeDto['links'] = result_data.__dict__['links']
                knowledgeDto['countries'] = result_data.__dict__['countries']
                knowledgeDto['additional_answers'] = result_data.__dict__['additional_answers']
                knowledgeDto['additional_links'] = result_data.__dict__['additional_links']
                results_dto.insert(0, knowledgeDto)

        self.logManager.add_log(
            type='[GOT] Answer',
            message=f'Got answer for {question} question. Answer ${json.dumps(results_dto)}',
            info='get_answers'
        )

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


class KnowledgeDAL:
    def __init__(self, db):
        self.db = db
        with open('knowledge/knowledge_metadata.json') as f:
            self.knowledgeMetaJsonData = json.load(f)

    def get_meta_all_data(self):
        return self.knowledgeMetaJsonData

    def get_meta_categories(self):
        return self.knowledgeMetaJsonData['categories']

    def get_all_data(self):
        return self.db.session.query(KnowledgeSchema).all()

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
            self.db.session.add(new_knowledge)
            self.db.session.commit()
            return 'Success'
        except:
            raise Exception('x should not exceed 5. The value of x was: {}'.format(x))
