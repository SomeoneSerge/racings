from racings import tools
from racings.domain import DOMAIN
from eve import Eve
import click


DOMAIN = tools.pyrsistent_to_mutable(DOMAIN)


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj['DEBUG'] = debug


@cli.command()
@click.pass_context
def run(ctx):
    app = Eve(settings=dict(
        DOMAIN=DOMAIN,
        RESOURCE_METHODS=['GET', 'POST', 'DELETE'],
        ITEM_METHODS=['GET', 'PATCH', 'DELETE']
    ))
    app.run()


@cli.command()
def print_schema():
    from racings_app import settings
    import pprint
    pprint.pprint(settings.DOMAIN)


if __name__ == '__main__':
    cli(obj={})
