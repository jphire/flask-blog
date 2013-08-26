# -*- coding: utf-8 -*-

from setuptools import setup

project = "fbone"

setup(
    name=project,
    version='0.1',
    url='https://github.com/imwilsonxu/fbone',
    description='this is a simple blog application, with multiple-logged in user support',
    author='Janne Laukkanen',
    author_email='janne.laukkanen83@gmail.com',
    packages=["fbone"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-WTF<=0.8.4',
        'Flask-Script',
        'Flask-Babel',
        'Flask-Testing',
        'Flask-Mail',
        'Flask-Cache',
        'Flask-Login',
        'Flask-OpenID',
        'nose',
        'psycopg2',
        'SQLAlchemy-Searchable',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)
