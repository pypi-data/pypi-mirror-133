import click
import subprocess


@click.command()
@click.argument('repo')
def dockerhub_list_tags(repo):
    """List tags in DockerHub"""
    rc = subprocess.call(["./resources/dockerhub_list_tags.sh", repo])
    print(f'dockerhub_list_tags.sh')
