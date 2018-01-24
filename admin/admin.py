from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import random
import click

from racings.domain import Base
from racings import domain


app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.randint(10**5, 10**10))
app.config['DATABASE_FILE'] = 'racings.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                       echo=True)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

admin = Admin(app, name='racings', template_mode='bootstrap3')
admin.add_view(ModelView(domain.Body, session))
admin.add_view(ModelView(domain.DriversLic, session))
admin.add_view(ModelView(domain.ScrutLic, session))
admin.add_view(ModelView(domain.User, session))
admin.add_view(ModelView(domain.Homologation, session))
admin.add_view(ModelView(domain.Manufacturer, session))
admin.add_view(ModelView(domain.CarPassport, session))
admin.add_view(ModelView(domain.Picture, session))

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    Base.metadata.create_all(engine)
    click.echo('Initialized the database')


@cli.command()
@click.option('--debug', is_flag=True)
def admin(debug=False):
    app.run(debug=debug)

if __name__ == '__main__':
    cli()
