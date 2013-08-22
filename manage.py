# -*- coding: utf-8 -*-

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

# BlogPost.author = relationship(User, backref=backref('posts', lazy='dynamic'))

@manager.command
def run():
    """Run in local machine."""

    app.run(debug=True, host='0.0.0.0', port=5050)


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            password=u'123456',
            role_code=ADMIN,
            status_code=ACTIVE,
            user_detail=UserDetail(
                sex_code=MALE,
                age=10,
                url=u'http://admin.example.com',
                deposit=100.00,
                location=u'Hangzhou',
                bio=u'admin Guy is ... hmm ... just a admin guy.'))

    test_user = User(
            name=u'test',
            email=u'test@example.com',
            password=u'123456',
            role_code=USER,
            status_code=ACTIVE,
            user_detail=UserDetail(
                sex_code=MALE,
                age=29,
                url=u'http://test.example.com',
                deposit=100.00,
                location=u'Hangzhou',
                bio=u'test user guy..'))

    db.session.add(admin)
    db.session.add(test_user)
    db.session.commit()
    
    admin = db.session.query(User).\
        filter_by(name='admin').\
        one() 
    
    erkki = db.session.query(User).\
        filter_by(name='test').\
        one()

    body = """
           Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.
           """
    for i in range(1, 10):
        post = BlogPost(
                        headline="Admin's Blog Post#{i}",
                        body=body,
                        user_id=admin.id)
        db.session.add(post)
    
    for i in range(1, 10):
        post = BlogPost(
                        headline="Erkki's Blog Post #{ i }",
                        body=body,
                        user_id=erkki.id)
        db.session.add(post)
    
    db.session.commit()

    tag1 = Tag(
               tag_name='tag1')
    tag2 = Tag(
               tag_name='tag2')

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.commit()

    tags = [tag1, tag2]
    post1 = db.session.query(BlogPost).\
        filter_by(id=1).\
        one()

    post1.tags = tags
    db.session.add(post1)
    db.session.commit()

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
