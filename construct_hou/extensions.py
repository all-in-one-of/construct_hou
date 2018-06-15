# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = ['Houdini']

from os.path import join, dirname, basename, isfile
from construct.extension import HostExtension
from construct_hou.tasks import (
    setup_construct_hou
)
from construct_launcher.constants import BEFORE_LAUNCH


class Version(list):

    @property
    def major(self):
        return self[0]

    @property
    def minor(self):
        return self[1]

    @property
    def build(self):
        return self[2]


class Houdini(HostExtension):
    '''Construct Houdini Host Extension

    Implements the HostExtension Interface. Provides a default hou workspace
    template and a launch task.
    '''

    name = 'Houdini'
    attr_name = 'houdini'

    def available(self, ctx):
        return True

    def load(self):

        self.add_template_path(join(dirname(__file__), 'templates'))
        self.add_task(
            'launch.houdini*',
            setup_construct_hou,
            priority=BEFORE_LAUNCH
        )

    @property
    def version(self):
        import hou
        if not hasattr(self, '_version'):
            setattr(self, '_version', Version(hou.applicationVersion()))
        return self._version

    def modified(self):
        import hou
        return (
            hou.hipFile.hasUnsavedChanges() and
            isfile(self.get_filename())
        )

    def save_file(self, file):
        import hou
        from construct_ui.dialogs import ask

        if self.modified():
            if ask('Would you like to save?', title='Unsaved changes'):
                hou.hipFile.save()

        hou.hipFile.save(file)

    def open_file(self, file):
        import hou
        from construct_ui.dialogs import ask

        if self.modified():
            if ask('Would you like to save?', title='Unsaved changes'):
                hou.hipFile.save()

        hou.load(file, suppress_save_prompt=True)

    def get_selection(self):
        import hou
        return hou.selectedNodes()

    def set_selection(self, selection):
        for node in self.get_selection():
            node.setSelected(False)
        for node in selection:
            node.setSelected(True)

    def get_workspace(self):
        import os
        return os.environ['JOB']

    def set_workspace(self, directory):
        import os
        os.environ['JOB'] = directory

    def get_filepath(self):
        import hou
        return hou.hipFile.path()

    def get_filename(self):
        import hou
        return basename(hou.hipFile.path())

    def get_frame_range(self):
        import hou
        if self.version > 15:
            frame_range = hou.playbar.frameRange()
        else:
            frame_range = hou.playbar.timelineRange()
        return frame_range[0], frame_range[1]

    def set_frame_range(self, start_frame, end_frame):
        import hou
        if self.version > 15:
            hou.setFrameRange(start_frame, end_frame)
        else:
            # TODO: This is wrong, how do we set global range in h15
            hou.setPlaybackRange(start_frame, end_frame)

    def get_qt_parent(self):
        import hou
        if self.version.major > 15:
            return hou.qt.mainWindow()
        else:
            return hou.ui.mainQtWindow()
