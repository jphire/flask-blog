# -*- coding: utf-8 -*-

import os

from flask import (Blueprint, render_template, send_from_directory,
                  abort, request, flash, redirect, url_for)
from flask import current_app as APP
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, current_user

from ..extensions import db

from ..user.models import User
from ..blogpost.models import BlogPost
from .models import Tag

from .forms import CreateTagForm, EditTagForm

tag = Blueprint('tag', __name__, url_prefix='/tag')

@tag.route('/')
def index():
    pagination = None
    if tags:
        page = int(request.args.get('page', 1))
        pagination = Tag.search(tags).paginate(page, 10)
    else:
        page = int(request.args.get('page', 1))
        pagination = Tag.search('').paginate(page, 10, False)

    return render_template('tag/index.html', pagination=pagination)

@login_required
@tag.route('/new', methods=['GET', 'POST'])
def create():
    
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))

    form = CreateTagForm(next=request.args.get('next'))

    if form.validate_on_submit():
        tag = Tag()
        tag.name = form.name.data
        
        db.session.add(tag)
        db.session.commit()
        flash(_('New tag created!'), 'success')
        return redirect(url_for('frontend.index'))

    return render_template('tags/create.html', form=form)

@login_required
@tag.route('/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit(tag_id):
    tag = Tag.get_by_id(tag_id)
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))

    form = EditTagForm(next=request.args.get('next'), obj=tag)

    if form.validate_on_submit():
        tag.tag_name = form.tag_name.data
        
        db.session.add(tag)
        db.session.commit()
        flash(_('Tag saved!'), 'success')
        return redirect(url_for('frontend.index'))

    return render_template('tags/edit.html', form=form, tag=tag)