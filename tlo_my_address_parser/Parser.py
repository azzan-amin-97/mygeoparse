"""
 Malaysian Address Parser
"""
import numpy as np

from tlo_my_address_parser.utils import execute_parsing_address_all, execute_parsing_address_one


class MalaysianAddressParser:

    def __init__(self, debug=False):
        self.debug = debug

        if self.debug:
            print('Parameters')
            print("=" * 40)
            print('Debug:', self.debug)
            print("=" * 40)

    def parser(self, args):
        result = np.nan
        if isinstance(args, str):
            result = execute_parsing_address_one(args)

        if isinstance(args, list):
            result = execute_parsing_address_all(args)
        return result
