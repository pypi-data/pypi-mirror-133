'''Project Short Description (default ini)

Project long description or extended summary goes in here (default ini)
'''


import argparse
import configparserext
import logging
from pathlib import Path

# import sys
from termcolor import colored
from beetools import beeutils
from beetools.beearchiver import Archiver


_PROJ_DESC = __doc__.split('\n')[0]
_PROJ_PATH = Path(__file__)


def project_desc():
    return _PROJ_DESC


class ProdigyHelmsman:
    '''Class description'''

    def __init__(self, p_ini_pth, p_logger=False):
        '''Method description'''
        self.success = True
        self.ini_pth = p_ini_pth
        self.logger_name = None
        self.logger = None
        if p_logger:
            self.logger_name = ProdigyHelmsman
            self.logger = logging.getLogger(self.logger_name)
        self.ini = configparserext.ConfigParserExt(
            self.logger_name, inline_comment_prefixes='#'
        )
        self.verbose = False

        self.ini.read([self.ini_pth])
        self.proj_root_dir = _PROJ_PATH.parents[1]

    def test_func(self):
        '''Method description'''
        print(colored('Testing ProdigyHelmsman...', 'yellow'))
        return True

    def run(self):
        '''Method description'''
        self.test_func()
        pass


def init_logger():
    logger = logging.getLogger(ProdigyHelmsman)
    logger.setLevel(beeutils.DEF_LOG_LEV)
    file_handle = logging.FileHandler(beeutils.LOG_FILE_NAME, mode='w')
    file_handle.setLevel(beeutils.DEF_LOG_LEV_FILE)
    console_handle = logging.StreamHandler()
    console_handle.setLevel(beeutils.DEF_LOG_LEV_CON)
    file_format = logging.Formatter(
        beeutils.LOG_FILE_FORMAT, datefmt=beeutils.LOG_DATE_FORMAT
    )
    console_format = logging.Formatter(beeutils.LOG_CONSOLE_FORMAT)
    file_handle.setFormatter(file_format)
    console_handle.setFormatter(console_format)
    logger.addHandler(file_handle)
    logger.addHandler(console_handle)


def read_args():
    arg_parser = argparse.ArgumentParser(description='Get configuration parameters')
    arg_parser.add_argument(
        'project_name',
        nargs='+',
        help='Project name',
    )
    arg_parser.add_argument(
        '-c',
        '--config-path',
        help='Config file name',
        default=arg_parser.prog[: arg_parser.prog.find('.') + 1] + 'ini',
    )
    arg_parser.add_argument(
        '-e', '--arc-extern-dir', help='Path to external archive', default=None
    )
    args = arg_parser.parse_args()
    arc_extern_dir = args.arc_extern_dir
    ini_path = args.config_path
    project_name = args.project_name[0]
    return project_name, ini_path, arc_extern_dir


if __name__ == '__main__':
    project_name, ini_pth, arc_extern_dir = read_args()
    init_logger()
    b_tls = Archiver(
        _PROJ_DESC,
        _PROJ_PATH,
        p_app_ini_file_name=ini_pth,
        p_arc_extern_dir=arc_extern_dir,
    )
    b_tls.print_header(p_cls=False)
    t_prodigyhelmsman = ProdigyHelmsman(ini_pth)
    if t_prodigyhelmsman.success:
        t_prodigyhelmsman.run()
    b_tls.print_footer()
# end __main__
