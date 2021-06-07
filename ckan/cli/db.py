# encoding: utf-8

import inspect
import logging
import os
import contextlib

import click
from itertools import groupby

import ckan.migration as migration_repo
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.model as model

log = logging.getLogger(__name__)

applies_to_plugin = click.option(u"-p", u"--plugin", help=u"Affected plugin.")


@click.group()
def db():
    """Database management commands.
    """
    pass


@db.command()
def init():
    """Initialize the database.
    """
    log.info(u"Initialize the Database")
    try:
        import ckan.model as model
        model.repo.init_db()
    except Exception as e:
        tk.error_shout(e)
    else:
        click.secho(u'Initialising DB: SUCCESS', fg=u'green', bold=True)


PROMPT_MSG = u'This will delete all of your data!\nDo you want to continue?'


@db.command()
@click.confirmation_option(prompt=PROMPT_MSG)
def clean():
    """Clean the database.
    """
    try:
        import ckan.model as model
        model.repo.clean_db()
    except Exception as e:
        tk.error_shout(e)
    else:
        click.secho(u'Cleaning DB: SUCCESS', fg=u'green', bold=True)


@db.command()
@click.option(u'-v', u'--version', help=u'Migration version', default=u'head')
@applies_to_plugin
def upgrade(version, plugin):
    """Upgrade the database.
    """
    _run_migrations(plugin, version, True)
    click.secho(u'Upgrading DB: SUCCESS', fg=u'green', bold=True)


@db.command()
@click.option(u'-v', u'--version', help=u'Migration version', default=u'base')
@applies_to_plugin
def downgrade(version, plugin):
    """Downgrade the database.
    """
    _run_migrations(plugin, version, False)
    click.secho(u'Downgrading DB: SUCCESS', fg=u'green', bold=True)


def _run_migrations(plugin, version, forward):
    if not version:
        version = 'head' if forward else 'base'
    with _repo_for_plugin(plugin) as repo:
        if forward:
            repo.upgrade_db(version)
        else:
            repo.downgrade_db(version)


@db.command()
@applies_to_plugin
def version(plugin):
    """Returns current version of data schema.
    """
    current = current_revision(plugin)
    try:
        current = _version_hash_to_ordinal(current)
    except ValueError:
        pass
    click.secho(u'Current DB version: {}'.format(current),
                fg=u'green',
                bold=True)


def current_revision(plugin):
    with _repo_for_plugin(plugin) as repo:
        repo.setup_migration_version_control()
        return repo.current_version()


@db.command(u"duplicate_emails", short_help=u"Check users email for duplicate")
def duplicate_emails():
    u'''Check users email for duplicate'''
    log.info(u"Searching for accounts with duplicate emails.")

    q = model.Session.query(model.User.email,
                            model.User.name) \
        .filter(model.User.state == u"active") \
        .filter(model.User.email != u"") \
        .order_by(model.User.email).all()

    if not q:
        log.info(u"No duplicate emails found")
    try:
        for k, grp in groupby(q, lambda x: x[0]):
            users = [user[1] for user in grp]
            if len(users) > 1:
                s = u"{} appears {} time(s). Users: {}"
                click.secho(
                    s.format(k, len(users), u", ".join(users)),
                    fg=u"green", bold=True)
    except Exception as e:
        tk.error_shout(e)


def _version_hash_to_ordinal(version):
    if u'base' == version:
        return 0
    versions_dir = os.path.join(os.path.dirname(migration_repo.__file__),
                                u'versions')
    versions = sorted(os.listdir(versions_dir))

    # latest version looks like `123abc (head)`
    if version.endswith(u'(head)'):
        return int(versions[-1].split(u'_')[0])
    for name in versions:
        if version in name:
            return int(name.split(u'_')[0])
    tk.error_shout(u'Version `{}` was not found in {}'.format(
        version, versions_dir))


def _resolve_alembic_config(plugin):
    if plugin:
        plugin_obj = p.get_plugin(plugin)
        if plugin_obj is None:
            tk.error_shout(u"Plugin '{}' cannot be loaded.".format(plugin))
            raise click.Abort()
        plugin_dir = os.path.dirname(inspect.getsourcefile(type(plugin_obj)))

        # if there is `plugin` folder instead of single_file, find
        # plugin's parent dir
        ckanext_idx = plugin_dir.rfind(u"/ckanext/") + 9
        idx = plugin_dir.find(u"/", ckanext_idx)
        if ~idx:
            plugin_dir = plugin_dir[:idx]
        migration_dir = os.path.join(plugin_dir, u"migration", plugin)
    else:
        import ckan.migration as _cm
        migration_dir = os.path.dirname(_cm.__file__)
    return os.path.join(migration_dir, u"alembic.ini")


@contextlib.contextmanager
def _repo_for_plugin(plugin):
    import ckan.model as model
    original = model.repo._alembic_ini
    model.repo._alembic_ini = _resolve_alembic_config(plugin)
    try:
        yield model.repo
    finally:
        model.repo._alembic_ini = original
