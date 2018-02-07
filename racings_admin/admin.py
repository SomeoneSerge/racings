from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import random
import click

from racings import model
from racings.model import DOMAIN

app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.randint(10**5, 10**10))
app.config['DATABASE_FILE'] = 'racings.db'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + app.config['DATABASE_FILE'])

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

admin = Admin(app, name='racings', template_mode='bootstrap3')
for v in model.EXPOSED.values():
    print(v)
    admin.add_view(ModelView(v, session))


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    DOMAIN.Base.metadata.create_all(engine)
    click.echo('Initialized the database')


@cli.command()
def filldb():
    DOMAIN.Base.metadata.create_all(engine)
    superuser = DOMAIN.Person(
        name='Noone',
        phone='1000000000',
        email='noone@nowhere.me',
        address='Nonexistence')
    scrutineers = DOMAIN.DocType(
        name='Scrutineer\'s License',
        person_variables=[
            DOMAIN.PersonVar(name='holder'),
            DOMAIN.PersonVar(name='issuer')
        ])
    drivers = DOMAIN.DocType(
        name='Driver\'s License',
        person_variables=[
            DOMAIN.PersonVar(name='holder'),
            DOMAIN.PersonVar(name='issuer')
        ])
    homologations = DOMAIN.DocType(
        name='Homologation',)
    seals = DOMAIN.DocType(
        name='Seal',)
    session.add_all([superuser, scrutineers, drivers, seals, homologations])
    session.commit()


@cli.command()
@click.option('--debug', is_flag=True)
def admin(debug=False):
    app.run(debug=debug)


if __name__ == '__main__':
    cli()
