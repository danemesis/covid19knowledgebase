from project import db
from project.tables import LogsSchema


class LogsManager:
    def __init__(self):
        self.logsDAL = LogsDAL()

    def get_all(self):
        results_dal = self.logsDAL.get_all()
        results_dto = []

        for result_dal in results_dal:
            logDto = {}
            logDto['type'] = result_dal.__dict__['type']
            logDto['message'] = result_dal.__dict__['message']
            logDto['info'] = result_dal.__dict__['info']
            results_dto.insert(0, logDto)

        return results_dto

    def add_log(self,
                type,
                message,
                info):
        return self.logsDAL.add_log(
            type=type,
            message=message,
            info=info
        )


class LogsDAL:
    def add_log(self,
                type,
                message,
                info):
        new_log = LogsSchema(
            type='GET',
            message='Getting all meta',
            info='get_meta_all_data'
        )
        try:
            db.session.add(new_log)
            return db.session.commit()
        except:
            print('Could not create a log')

    def get_all(self):
        return db.session.query(LogsSchema).order_by(LogsSchema.date_created).all()
