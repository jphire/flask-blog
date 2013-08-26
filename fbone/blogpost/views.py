# -*- coding: utf-8 -*-

import os

from flask import (Blueprint, render_template, send_from_directory,
                  abort, request, flash, redirect, url_for)
from flask import current_app as APP
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, current_user

from ..extensions import db

from ..user.models import User
from .models import BlogPost
from ..tag.models import Tag

from .forms import CreateBlogPostForm, EditBlogPostForm

blogpost = Blueprint('blogpost', __name__, url_prefix='/post')


@blogpost.route('/')
def index():
    tags = request.args.get('tags', '').strip()
    pagination = None
    if tags:
        page = int(request.args.get('page', 1))
        pagination = BlogPost.search(tags).paginate(page, 10)
    else:
        page = int(request.args.get('page', 1))
        pagination = BlogPost.search('').paginate(page, 10, False)

    return render_template('post/index.html', pagination=pagination, tags=tags)


@blogpost.route('/<int:post_id>/show')
def show(post_id):
    post = BlogPost.get_by_id(post_id)
    return render_template('post/show.html', post=post)

@login_required
@blogpost.route('/new', methods=['GET', 'POST'])
def create():
    
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))

    form = CreateBlogPostForm(next=request.args.get('next'))

    if form.validate_on_submit():
        post = BlogPost()
        post.headline = form.headline.data
        post.body = form.body.data
        u = User.get_by_id(current_user.id)
        post.author = u
        # post.tags = Tag()
        
        db.session.add(post)
        db.session.commit()
        flash(_('New post created!'), 'success')
        return redirect(url_for('frontend.index'))

    return render_template('post/create.html', form=form)

@login_required
@blogpost.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    post = BlogPost.get_by_id(post_id)
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))

    form = EditBlogPostForm(request.form, obj=post)
    form.tags.choices = [(g.id, g.tag_name) for g in Tag.query.filter(Tag.user_id==current_user.id).order_by('tag_name')]
    form.tags.data = [p.id for p in post.tags]

    if form.validate_on_submit():
        post.headline = form.headline.data
        post.body = form.body.data
        post.tags = Tag.query.filter(Tag.id.in_(request.form.getlist('tags'))).all()

        db.session.add(post)
        db.session.commit()
        flash(_('Post updated!'), 'success')
        return redirect(url_for('frontend.index'))
    
    return render_template('post/edit.html', form=form, post=post)

@login_required
@blogpost.route('/<int:post_id>/destroy', methods=['GET','POST'])
def destroy(post_id):
    post = BlogPost.get_by_id(post_id)
    if not current_user.is_authenticated():
        return redirect(url_for('frontend.index'))
    else:
        db.session.delete(post)
        db.session.commit()
        flash(_('Post removed!'), 'success')
        return redirect(url_for('frontend.index'))

    flash(_('Could not remove post!'), 'error')
    return redirect(url_for('frontend/index'))
