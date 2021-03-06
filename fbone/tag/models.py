# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, types, Table, ForeignKey

from ..extensions import db

class Tag(db.Model):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(50), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    @classmethod
    def get_by_id(cls, tag_id):
        return cls.query.filter_by(id=tag_id).first_or_404()