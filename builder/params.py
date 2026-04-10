import re
import time
import requests

from builder.header import HeaderBuilder

class Params:
    def __init__(self):
        self.params = {}

    def add_param_by_dict(self, params):
        self.params.update(params)

    def add_param(self, key, value):
        self.params[key] = value

    def get(self):
        return self.params


class ParamsBuilder:
    base_url = 'https://www.rootdata.com'

    @staticmethod
    def build_get_user_info_param():
        params = Params()
        params.add_param_by_dict({

        })
        return params

