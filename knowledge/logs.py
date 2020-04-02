from dto.log import LogDto
from knowledge.tables import LogsSchema


class LogsManager:
    def __init__(self, db):
        self.db = db
        self.logsDAL = LogsDAL(db)

    def get_all(self):
        results_dal = self.logsDAL.get_all()
        results_dto = []

        for result_dal in results_dal:
            results_dto.insert(
                0,
                LogDto(
                    type=result_dal.__dict__['type'],
                    message=result_dal.__dict__['message'],
                    info=result_dal.__dict__['info'],
                )
            )

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
    def __init__(self, db):
        self.db = db

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
            self.db.session.add(new_log)
            return self.db.session.commit()
        except:
            print('Could not create a log')

    def get_all(self):
        return self.db.session.query(LogsSchema).order_by(LogsSchema.date_created).all()
