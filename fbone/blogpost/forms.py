# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, BooleanField, TextField, TextAreaField,
        SubmitField, SelectMultipleField)
from flask.ext.wtf import Required, Length, EqualTo

class CreateBlogPostForm(Form):
    next = HiddenField()
    headline = TextField(u'Headline', [Required()])
    body = TextAreaField(u'Content', [Required(), Length(0, 10000)])
    submit = SubmitField('Create')

class EditBlogPostForm(Form):
    next = HiddenField()
    headline = TextField(u'Headline', [Required()])
    tags = SelectMultipleField(u'Tags', coerce=int)
    body = TextAreaField(u'Content', [Required(), Length(0, 10000)])
    submit = SubmitField('Save')