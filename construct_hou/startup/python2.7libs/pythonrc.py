# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging

import construct
from construct_hou import callbacks, utils


_log = logging.getLogger('construct.hou.pythonrc')
construct.init()
ctx = construct.get_context()
host = construct.get_host()

_log.debug('Setting workspace: %s' % ctx.workspace.path)
host.set_workspace(ctx.workspace.path)

_log.debug('Registering callbacks')
callbacks.register()

_log.debug('Creating Construct menu...')
# TODO


if utils.show_file_open_at_startup():
    # TODO: Add abstraction around creating ActionForms
    if ctx.workspace and not host.get_filename():
        action = construct.actions.get('file.open')
        parent = host.get_qt_parent()
        form_cls = construct.get_form(action.identifier)
        form = form_cls(action, ctx, parent)
        form.setStyleSheet(resources.style(':/styles/dark'))
        form.show()
