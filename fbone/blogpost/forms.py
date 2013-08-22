# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, BooleanField, TextField, TextAreaField,
        SubmitField)
from flask.ext.wtf import Required, Length, EqualTo

class CreateBlogPostForm(Form):
    next = HiddenField()
    headline = TextField(u'Headline', [Required()])
    body = TextAreaField(u'Content', [Required(), Length(0, 1000)])
    submit = SubmitField('Create')

class EditBlogPostForm(Form):
    next = HiddenField()
    headline = TextField(u'Headline', [Required()])
    body = TextAreaField(u'Content', [Required(), Length(0, 1000)])
    submit = SubmitField('Save')