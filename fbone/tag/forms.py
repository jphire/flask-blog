# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, BooleanField, TextField,
        SubmitField)
from flask.ext.wtf import Required, Length, EqualTo

class CreateTagForm(Form):
    next = HiddenField()
    tag_name = TextField(u'Tagname', [Required()])
    submit = SubmitField('Create')

class EditTagForm(Form):
    next = HiddenField()
    tag_name = TextField(u'Tagname', [Required()])
    submit = SubmitField('Save')