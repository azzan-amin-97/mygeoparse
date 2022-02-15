"""
 Malaysian Address Parser
"""
import numpy as np

from tlo_my_address_parser.utils import execute_parsing_address_all, execute_parsing_address_one


class MalaysianAddressParser:
    house_number = ""
    building_name = ""
    street_name = ""
    postcode = ""
    state = ""

    def __init__(self, full_address, debug=False):
        self.debug = debug
        self.full_address = full_address

        if self.debug:
            print('Parameters')
            print("=" * 40)
            print('Debug:', self.debug)
            print("=" * 40)



    def parser(self, args):
        result = np.nan

        if isinstance(args, str):
            result = execute_parsing_address_one(args)

        elif isinstance(args, list):
            result = execute_parsing_address_all(args)
            return result

        return result
