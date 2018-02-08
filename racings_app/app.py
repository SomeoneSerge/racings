from racings import tools
from racings.domain import DOMAIN
from eve import Eve
from pymongo import MongoClient
import click

DOMAIN = tools.pyrsistent_to_mutable(DOMAIN)


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--mongo-host', default='127.0.0.1')
@click.option('--mongo-port', default=27017)
@click.option('--mongo-user', default='')
@click.option('--mongo-pass', default='')
@click.option('--mongo-db', default='racings')
@click.pass_context
def cli(ctx, debug, mongo_host, mongo_port, mongo_user, mongo_pass, mongo_db):
    ctx.obj = dict(
        DEBUG=debug,
        MONGO_HOST=mongo_host,
        MONGO_PORT=mongo_port,
        MONGO_DBNAME=mongo_db,
        DOMAIN=DOMAIN,
        RESOURCE_METHODS=['GET', 'POST', 'DELETE'],
        ITEM_METHODS=['GET', 'PATCH', 'DELETE'])
    if mongo_user is not None and mongo_user != '':
        ctx.obj += m(
            MONGO_USERNAME=mongo_user,
            MONGO_PASSWORD=mongo_pass)


@cli.command()
@click.pass_context
def run(ctx):
    app = Eve(settings=ctx.obj)
    app.run()


@cli.command()
def print_schema():
    import pprint
    pprint.pprint(DOMAIN)


@cli.command()
@click.option('--clean/--no-clean', default=False)
@click.pass_context
def filldb(ctx, clean):
    from racings.examples import SAMPLE_DATA
    settings = ctx.obj
    if 'MONGO_USERNAME' in settings:
        kwargs = m(
            username=settings['MONGO_USERNAME'],
            password=settings['MONGO_PASSWORD'])
    else:
        kwargs = {}
    db = MongoClient(
        settings['MONGO_HOST'],
        settings['MONGO_PORT'],
        **kwargs
        )
    db = db[settings['MONGO_DBNAME']]
    for k in SAMPLE_DATA:
        collection = db[k]
        if clean:
            collection.delete_many({})
        collection.insert_many(SAMPLE_DATA[k])


if __name__ == '__main__':
    cli(obj={})
