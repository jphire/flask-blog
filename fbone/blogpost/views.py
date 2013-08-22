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

    form = EditBlogPostForm(next=request.args.get('next'), obj=post)

    if form.validate_on_submit():
        # post.tags = Tag()
        post.headline = form.headline.data
        post.body = form.body.data

        db.session.add(post)
        db.session.commit()
        flash(_('Post saved!'), 'success')
        return redirect(url_for('frontend.index'))

    return render_template('post/edit.html', form=form, post=post)