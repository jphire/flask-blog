# -*- coding: utf-8 -*-

import os

from flask import (Blueprint, render_template, send_from_directory,
                  abort, request, flash, redirect, url_for, jsonify)
from flask import current_app as APP
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, current_user

from ..extensions import db

from ..user.models import User
from ..blogpost.models import BlogPost
from .models import Tag

from .forms import CreateTagForm, EditTagForm

tag = Blueprint('tag', __name__, url_prefix='/tag')

@login_required
@tag.route('/')
def index():
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))
        
    all_tags = Tag.query.all()

    return render_template('tags/index.html', all_tags=all_tags)

@login_required
@tag.route('/new', methods=['GET', 'POST'])
def create():
    post_id = request.form['post_id']
    tag_name = request.form['tag_name']
    
    post = BlogPost.get_by_id(post_id)
    
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))
    else:
        tag = Tag()
        tag.tag_name = tag_name
        post.tags = post.tags + [tag]

        db.session.add(tag)
        db.session.commit()
        return jsonify(result=tag.tag_name)

    return jsonify(result='error')

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


@login_required
@tag.route('/<int:tag_id>/destroy', methods=['GET','POST'])
def destroy(tag_id):
    tag = Tag.get_by_id(tag_id)
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))
    else:
        db.session.delete(tag)
        db.session.commit()
        flash(_('Tag removed!'), 'success')
        return redirect(url_for('.index'))
    
    all_tags = Tag.query.all()
    return render_template('tags/index.html', all_tags=all_tags)
