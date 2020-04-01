import json

from fuzzywuzzy import fuzz


class KnowledgeManager:
    def __init__(self):
        self.knowledge = Knowledge()

    def get_json_basic_functionality(self):
        return self.knowledge.get_json_basic_functionality()

    def get_json_data(self):
        return self.knowledge.get_json_all_data()

    def get_categories(self):
        return self.knowledge.get_categories()

    def get_answers(self, question):
        return self.knowledge.get_answers(question)


class Knowledge:
    def __init__(self):
        with open('knowledge/base.json') as f:
            self.jsonData = json.load(f)
        self.arrayData = self.jsonData.items()

        with open('knowledge/base_knowledge_meta.json') as f:
            self.baseKnowledgeMetaJsonData = json.load(f)


    def get_json_basic_functionality(self):
        return self.baseKnowledgeMetaJsonData

    def get_json_all_data(self):
        return self.jsonData

    def get_categories(self):
        results = []

        for attribute, value in self.arrayData:
            category = value['category']
            if category not in results:
                results.insert(0, category)

        return results

    def get_answers(self, question):
        results = []

        for dbQuestion, value in self.arrayData:
            if fuzz.token_set_ratio(dbQuestion, question) > 95:
                results.insert(1, value)

        return results
