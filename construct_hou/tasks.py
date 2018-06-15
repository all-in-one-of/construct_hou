# -*- coding: utf-8 -*-
from __future__ import absolute_import

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
    old_pypath = app.env.get('PYTHONPATH', '')
    pypath = os.pathsep.join([
        hou_path,
        os.path.join(os.path.dirname(__file__), '..')
    ])
    if old_pypath:
        pypath += os.pathsep + old_pypath

    app.env['HOUDINI_PATH'] = hou_path
    app.env['PYTHONPATH'] = pypath