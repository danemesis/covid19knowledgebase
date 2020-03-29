import json


class Data:
    def __init__(self):
        with open('flaskr/knowledgeBase/base.json') as f:
            self.data = json.load(f)

    def get_raw_data(self):
        return self.data

    def get_answers(self, question):
        results = []

        # for song in self.data:
        for attribute, value in self.data.items():
            if attribute == question:
                results.insert(1, value)

        return json.dumps(results)
