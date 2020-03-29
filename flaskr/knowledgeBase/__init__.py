import json


class Data:
    def __init__(self):
        with open('flaskr/knowledgeBase/base.json') as f:
            self.data = json.load(f)
        print('Loaded in memory', self.data)

    def show_data(self):
        return self.data
