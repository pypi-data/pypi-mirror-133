import os
import sys
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

from .utils import CmdUtil,IoUtil,StringUtil,PathUtil,FireUtil
from .config import PACKGAE_CONFIG_FILENAME,PACKGAE_CONFIG_FILENAME_YML
class Package:
    def __init__(self, path):
        self.path = os.path.abspath(path)

    def join_path(self, path):
        return os.path.join(self.path,path)

    def load_info(self):
        config_path = self.join_path(PACKGAE_CONFIG_FILENAME)
        config_path_yml = self.join_path(PACKGAE_CONFIG_FILENAME_YML)
        if os.path.exists(config_path):
            return IoUtil.json_load(config_path)
        elif os.path.exists(config_path_yml):
            return IoUtil.yaml_load(config_path_yml)
        else:
            return None
    def cmd_in_path(self,command):
        return CmdUtil.run_multiple_commands(['cd %s'%(self.path),command])
    def install_dependencies(self):
        cfg = self.load_info()
        if cfg:
            dependencies = cfg['dependencies']
            try:
                pkg_resources.require(dependencies)
            except DistributionNotFound:
                for pkg in dependencies:
                    self.cmd_in_path([sys.executable,'-m','pip','install',pkg])
            except VersionConflict:
                raise VersionConflict

    def run(self, args):
        path = self.path
        entry_filepath = os.path.join(path, 'entry.py')
        fire_filepath = os.path.join(path, 'firex.py')
        if os.path.exists(entry_filepath):
            CmdUtil.run_file(entry_filepath, args)
        elif os.path.exists(fire_filepath):
            CmdUtil.run_file(fire_filepath, args,fire=True)
        else:
            os.chdir(path)
            CmdUtil.run_command(['pkman', *args])