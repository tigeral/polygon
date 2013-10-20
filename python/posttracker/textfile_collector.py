# coding=utf-8

import string
import logging

DEFAULT_DATA_FILE_NAME = "codes.txt"

logger = logging.getLogger('collector')

class Collector:
    def __init__(self, config):
        # initialize default values
        self.dataFileName = DEFAULT_DATA_FILE_NAME

        # override default values with values from config file
        self._process_config(config)

    def _process_config(self, config):
        if config.has_option("collector", "data_file_name"):
            self.dataFileName = config.get("collector", "data_file_name")

    def get_next_code(self):
        return None

    def get_all_codes(self):
        result_list = []
        data_file = open(self.dataFileName)
        file_lines = data_file.readlines()
        for line in file_lines:
            line_data = string.split(line, ":", 1)
            code_item = {"code": line_data[0], "description": line_data[1]}
            result_list.append(code_item)
        return result_list