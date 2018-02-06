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
    'sqlite:///' + app.config['DATABASE_FILE']
)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                       echo=True)
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
    # root_body = domain.Body(
    #     id=1,
    #     name='Superuser',
    #     phone='+11234567890',
    #     email='root@racings.local')
    # root_user = domain.User(id=root_body.id, login='root', pw='qwerty')
    # root_driver = domain.ScrutLic(licensee=root_body.id, issuer=root_body.id,)
    # session.add_all([root_body, root_user, root_driver])
    session.commit()



@cli.command()
@click.option('--debug', is_flag=True)
def admin(debug=False):
    app.run(debug=debug)

if __name__ == '__main__':
    cli()
