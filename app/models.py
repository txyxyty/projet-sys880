from . import db
from datetime import datetime as dt


class RobotData(db.Model):
    __tablename__ = 'robot_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bot = db.Column(db.JSON, nullable=False)
    persons = db.Column(db.JSON, nullable=False)
    datetime = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=dt.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'bot': self.bot,
            'persons': self.persons,
            'datetime': self.datetime,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
