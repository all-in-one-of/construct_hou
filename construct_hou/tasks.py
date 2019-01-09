# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__all__ = [
    'setup_construct_hou',
]

import os
from construct.utils import unipath
from construct.tasks import (
    task,
    requires,
    success,
    params,
    store
)


@task
@requires(success('build_app_env'))
@params(store('app'))
def setup_construct_hou(app):
    '''Setup Houdini environment'''

    hou_path = unipath(os.path.dirname(__file__), 'startup')
    old_hou_path = app.env.get('HOUDINI_PATH', None)
    if old_hou_path:
        hou_path += os.pathsep + old_hou_path

    old_pypath = app.env.get('PYTHONPATH', None)
    pypath = os.pathsep.join([
        hou_path,
        os.path.join(os.path.dirname(__file__), '..')
    ])
    if old_pypath:
        pypath += os.pathsep + old_pypath

    app.env['HOUDINI_PATH'] = hou_path
    app.env['PYTHONPATH'] = pypath
