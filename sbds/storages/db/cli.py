# -*- coding: utf-8 -*-

import json

import click

import sbds.logging
from sbds.storages.db import Base
from sbds.storages.db import Session
from sbds.storages.db import add_blocks
from sbds.storages.db import bulk_add
from sbds.storages.db.tables import init_tables
from sbds.storages.db.tables import reset_tables
from sbds.storages.db.tables import test_connection
from sbds.storages.db.utils import configure_engine
from sbds.storages.db.utils import get_db_processes
from sbds.storages.db.utils import kill_db_processes
from sbds.storages.db.utils import row_to_json
from sbds.utils import chunkify

logger = sbds.logging.getLogger(__name__)


@click.group(short_help='Interact with an SQL storage backend')
@click.option(
    '--database_url',
    type=str,
    envvar='DATABASE_URL',
    help='Database connection URL in RFC-1738 format, read from "DATABASE_URL" ENV var by default'
)
@click.option('--echo', is_flag=True)
@click.pass_context
def db(ctx, database_url, echo):
    """Interact with an SQL storage backend
        Typical usage would be reading blocks in JSON format from STDIN
        and then storing those blocks in the database:

        \b
            sbds | db insert-blocks

        In the example above, the "sbds" command streams new blocks to STDOUT, which are piped to STDIN of
        the "db insert-blocks" command by default. The "database_url" was read from the "DATABASE_URL"
        ENV var, though it may optionally be provided on the command line:

        \b
        db --database_url 'dialect[+driver]://user:password@host/dbname[?key=value..]' tests

    """

    engine_config = configure_engine(database_url, echo=echo)

    ctx.obj = dict(
        database_url=engine_config.database_url,
        url=engine_config.url,
        engine_kwargs=engine_config.engine_kwargs,
        engine=engine_config.engine,
        base=Base,
        metadata=Base.metadata,
        Session=Session)


@db.command()
@click.pass_context
def test(ctx):
    """Test connection to database"""
    database_url = ctx.obj['database_url']
    url, table_count = test_connection(database_url)
    if url:
        click.echo('Success! Connected using %s, found %s tables' %
                   (url.__repr__(), table_count))
    else:
        click.echo('Failed to connect: %s', url)
        ctx.exit(code=127)


@db.command(name='insert-blocks')
@click.argument('blocks', type=click.File('r', encoding='utf8'), default='-')
@click.pass_context
def insert_blocks(ctx, blocks):
    """Insert blocks into the database"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()

    add_blocks(blocks, session)


@db.command(name='bulk-add')
@click.argument('blocks', type=click.File('r', encoding='utf8'), default='-')
@click.option('--chunksize', type=click.INT, default=1000)
@click.pass_context
def bulk_add_blocks(ctx, blocks, chunksize):
    """Insert many blocks in the database"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()
    click.echo("SQL: 'SET SESSION innodb_lock_wait_timeout=150'", err=True)
    session.execute('SET SESSION innodb_lock_wait_timeout=150')

    try:
        for chunk in chunkify(blocks, chunksize):
            bulk_add(chunk, session)
    except Exception as e:
        raise e
    finally:
        session.close_all()


@db.command(name='init')
@click.pass_context
def init_db_tables(ctx):
    """Create any missing tables on the database"""
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    init_tables(database_url, metadata)


@db.command(name='reset')
@click.confirmation_option(
    prompt='Are you sure you want to drop and then create the db?')
@click.pass_context
def reset_db_tables(ctx):
    """Drop and then create tables on the database"""
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    reset_tables(database_url, metadata)


@db.command(name='list-processes')
@click.pass_context
def list_processes(ctx):
    """Create any missing tables on the database"""
    database_url = ctx.obj['database_url']

    processes = get_db_processes(database_url)
    for proc in processes:
        click.echo(row_to_json(proc))


@db.command(name='kill-processes')
@click.pass_context
def kill_processes(ctx):
    """Create any missing tables on the database"""
    database_url = ctx.obj['database_url']

    # pylint: disable=unused-variable
    processes, killed = kill_db_processes(database_url)
    # pylint: enable=unused-variable
    click.echo('killed %s processes' % len(killed))
    for proc in killed:
        click.echo(row_to_json(proc))


@db.command(name='last-block')
@click.pass_context
def last_block(ctx):
    """Return the highest block stored in the database"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()

    from sbds.storages.db.tables import Block
    click.echo(Block.highest_block(session))


@db.command(name='find-missing-blocks')
@click.pass_context
def find_missing_blocks(ctx):
    """Return JSON array of block_nums from missing blocks"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()

    from sbds.storages.db.tables import Block
    #click.echo(json.dumps(Block.find_missing(session)))


@db.command(name='add-missing-posts-and-comments')
@click.pass_context
def add_missing_posts_and_comments(ctx):
    """Add missing posts and comments from txcomments"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)

    from sbds.storages.db.tables import PostAndComment
    PostAndComment.add_missing(Session)


@db.command(name='find-missing-posts-and-comments')
@click.pass_context
def find_missing_posts_and_comments(ctx):
    """Return JSON array of block_nums from missing post and comment blocks"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()

    from sbds.storages.db.tables import PostAndComment
    block_nums = PostAndComment.find_missing_block_nums(session)
    click.echo(json.dumps(block_nums))
