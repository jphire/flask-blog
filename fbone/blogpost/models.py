# -*- coding: utf-8 -*-

import sqlalchemy as sa

from sqlalchemy import Column, Integer, String, types, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref

from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import Searchable, SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import search as ft_search

from ..extensions import db

post_tags = Table('post_tags', db.Model.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

# for full-text search
class PostQuery(BaseQuery, SearchQueryMixin):
    pass

class BlogPost(db.Model, Searchable):
    query_class = PostQuery
    __tablename__ = 'posts'
    __searchable_columns__ = ['headline', 'body']

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, ForeignKey('users.id'))
    headline = sa.Column(sa.Unicode(255), nullable=False)
    body = sa.Column(sa.UnicodeText)
    search_vector = sa.Column(TSVectorType)

    # many to many BlogPost<->Tag
    tags = relationship('Tag', secondary=post_tags, backref='posts')

    @classmethod
    def search(cls, query_str):
        return BlogPost.query.search(query_str)

    @classmethod
    def get_by_id(cls, post_id):
        return cls.query.filter_by(id=post_id).first_or_404()