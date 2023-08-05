# -*- coding: utf-8 -*-
# @author: leesoar
# @email: core@111.com

import argparse

from thunders import __version__

parser = argparse.ArgumentParser(description=f"thunders", prog="thunders", add_help=False)
parser.add_argument('-v', '--version', action='version', version=__version__, help='Get version of thunders')
parser.add_argument('-h', '--help', action='help', help='Show help message')
parser.parse_args()


def run():
    return "Powered by leesoar.com"
