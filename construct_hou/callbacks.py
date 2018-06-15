# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import construct

_log = logging.getLogger('construct.hou.callbacks')


def set_context_to_hou_scene():
    '''Sets the Context to the current houd scene, if it's in a workspace'''

    host = construct.get_host()
    path = host.get_filepath()

    new_ctx = construct.Context.from_path(path)
    new_ctx.file = path

    if new_ctx.workspace:
        _log.debug('Setting context to %s' % path)
        construct.set_context(new_ctx)
        new_ctx.to_env()
    else:
        _log.debug(
            'Not setting context. '
            'Scene is not in a construct workspace...'
        )


def scene_event_callback(event_type):
    '''Scene event callback'''

    import hou

    accepted_events = (
        hou.hipFileEventType.AfterLoad,
        hou.hipFileEventType.AfterSave,
    )
    if event_type in accepted_events:
        set_context_to_hou_scene()


def register():
    '''Register construct_hou callbacks'''

    import hou
    hou.hipFile.addEventCallback(scene_event_callback)
