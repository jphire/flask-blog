#!/usr/bin/env python

import os
import readline
from pprint import pprint

from flask import *

# from fbone import *
# from fbone.user import *
# from fbone.blogpost import *
# from fbone.tag import *
# from fbone import create_app
from flask.ext.script import Manager
from fbone import create_app
from fbone.extensions import db
from fbone.user import User, UserDetail, ADMIN, USER, ACTIVE
from fbone.tag import Tag
from fbone.blogpost import BlogPost
from fbone.utils import MALE
from sqlalchemy.orm import relationship, backref

app = create_app()
manager = Manager(app)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

manager.run()

os.environ['PYTHONINSPECT'] = 'True'