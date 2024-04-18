import click
from neomodel import config

from modul_graph.loader.pdf import data_loader


@click.group()
def main():
    pass


# NEOMODEL SETUP
config.DATABASE_URL = 'bolt://neo4j:dev_pw@localhost:7687'

data_loader()
