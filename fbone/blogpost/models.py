# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, types, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import Mutable
from flask.ext.login import UserMixin

from ..extensions import db

post_tags = Table('post_tags', db.Model.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class BlogPost(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    # many to many BlogPost<->Tag
    tags = relationship('Tag', secondary=post_tags, backref='posts')

    @classmethod
    def search(cls, tags):
        criteria = []
        if tags != '':
            for tag in tags.split():
                tag = '%' + tag + '%'
                criteria.append(db.or_(
                    BlogPost.headline.ilike(tag),
                ))
        else:
            return cls.query

        q = reduce(db.and_, criteria)
        return cls.query.filter(q)

    @classmethod
    def get_by_id(cls, post_id):
        return cls.query.filter_by(id=post_id).first_or_404()

