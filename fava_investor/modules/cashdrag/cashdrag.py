#!/usr/bin/env python3
# Description: CLI for cash drag

import argparse,argcomplete,argh
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common'))
import beancountinvestorapi as api

from clicommon import *
import libcashdrag

def cashdrag(beancount_file,
    accounts_pattern: 'Regex pattern of accounts to include in hunting cash drag.' = '',
    accounts_exclude_pattern: 'Regex pattern of accounts to exclude in hunting cash drag.' = '',
    debug=False):

    argsmap = locals()
    accapi = api.AccAPI(beancount_file, argsmap)
    if not accounts_pattern:
        del argsmap['accounts_pattern']
    if not accounts_exclude_pattern:
        del argsmap['accounts_exclude_pattern']
    rtypes, rrows, total = libcashdrag.find_loose_cash(accapi, argsmap)
    print("Total: {}".format(total))
    pretty_print_table(rtypes, rrows)


#-----------------------------------------------------------------------------
def main():
    parser = argh.ArghParser(description="Beancount Asset Cash Drag")
    argh.set_default_command(parser, cashdrag)
    argh.completion.autocomplete(parser)
    parser.dispatch()
    return 0

if __name__ == '__main__':
    main()
