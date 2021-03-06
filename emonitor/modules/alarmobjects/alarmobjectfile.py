import os
from flask import current_app
from sqlalchemy.sql import collate
from emonitor.extensions import db


class AlarmObjectFile(db.Model):
    """Files for alarmobjects"""
    __tablename__ = 'alarmobjectfile'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('alarmobjects.id'))
    filename = db.Column(db.String(80))
    filetype = db.Column(db.String(50))

    def __repr__(self):
        return "<alarmobjectfile %s>" % self.filename

    def __init__(self, objectid, filename, filetype):
        self.object_id = objectid
        self.filename = filename
        self.filetype = filetype

    @property
    def filesize(self):
        def sizeof_fmt(num):
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if num < 1024.0:
                    return "%3.1f %s" % (num, x)
                num /= 1024.0
        if os.path.exists('%salarmobjects/%s/%s' % (current_app.config.get('PATH_DATA'), self.object_id, self.filename)):
            return sizeof_fmt(os.stat('%salarmobjects/%s/%s' % (current_app.config.get('PATH_DATA'), self.object_id, self.filename)).st_size)
        return sizeof_fmt(0)

    @staticmethod
    def getFile(id, filename=""):
        """
        Get file(s) for alarmobject

        :param id: objectid as integer
        :param filename: filename as string
        :return: :py:class:`emonitor.modules.alarmobjects.alarmobjectfile.AlarmObjectFile`
        """
        if filename == "":
            return AlarmObjectFile.query.filter_by(id=id).first()
        else:
            return AlarmObjectFile.query.filter_by(object_id=id, filename=filename).first()

    @staticmethod
    def getAlarmObjectTypes(objectid=0):
        """
        Get all possible alarmobject types

        :param objectid: objectid as integer
        :return: list of :py:mod:`emonitor.modules.alarmobjects.alarmobjectfile.AlarmObjectFile`
        """
        if objectid != 0:
            return AlarmObjectFile.query.filter_by(id=objectid).all()
        else:
            return AlarmObjectFile.query.order_by(collate(AlarmObjectFile.name, 'NOCASE')).all()
