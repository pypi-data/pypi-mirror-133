import click


@click.group()
def cli():
    """Command line interface for the greet package"""
    pass

from .dockerhub_list_tags import dockerhub_list_tags
cli.add_command(dockerhub_list_tags)

if __name__ == '__main__':
    cli()
