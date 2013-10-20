# coding=utf-8

import ConfigParser
import importlib
import logging
import sys
import getopt
import argparse

DEFAULT_CONFIG_FILE_NAME = "default.conf"
DEFAULT_OUTPUT_FILE_NAME = "result.txt"
DEFAULT_COLLECTOR_MODULE_NAME = "textfile_collector"
DEFAULT_TRACKER_MODULE_NAME = "ukrpost_tracker"

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger('posttracker')
logger.addHandler(logging.StreamHandler())


class PostTracker:

    def __init__(self, cmdArgs):
        self.configFileName = DEFAULT_CONFIG_FILE_NAME
        self._collectorModuleFileName = DEFAULT_COLLECTOR_MODULE_NAME
        self._trackerModuleFileName = DEFAULT_TRACKER_MODULE_NAME

        if cmdArgs is not None:
            self._process_cmd_args(cmdArgs)

        self._process_config(self.configFileName)

        self._init_logger()
        self._init_modules()

    def get_all_codes_with_status(self):
        codes = self.collector.get_all_codes()
        for code in codes:
            status = self.tracker.get_status(code["code"])
            code["status"] = status
        return codes

    def _process_cmd_args(self, cmdArgs):
        parser = argparse.ArgumentParser(description='Find an information about post sending status.')
        parser.add_argument('-c, --config', metavar='file_name', default=DEFAULT_CONFIG_FILE_NAME,
                            dest='configFileName', help='config .ini like file, see default.conf for reference')
        parser.add_argument('-o, --output', metavar='file_name', default=DEFAULT_OUTPUT_FILE_NAME,
                            dest='outputFileName', help='file where the result data would be stored')

        args = parser.parse_args(cmdArgs)
        self.configFileName = args.configFileName
        self.outputFileName = args.outputFileName

    def _process_config(self, configFileName):
        config = ConfigParser.RawConfigParser()
        if len(config.read(configFileName)) == 0:
            logger.error("couldn't read a config file \"" + self.configFileName + "\"")
            exit(1)
        self.config = config

        # read what a program module used to get post codes to track
        if config.has_option("collector", "module"):
            self._collectorModuleFileName = config.get("collector", "module")

        # read what a program module used to get post codes to track
        if config.has_option("tracker", "module"):
            self._trackerModuleFileName = config.get("tracker", "module")

    def _init_modules(self):
        logger.info("initialize modules: " + self._collectorModuleFileName + ", " + self._trackerModuleFileName)

        self._collectorModule = importlib.import_module(self._collectorModuleFileName)
        self.collector = self._collectorModule.Collector(self.config)

        self._trackerModule = importlib.import_module(self._trackerModuleFileName)
        self.tracker = self._trackerModule.Tracker(self.config)

    def _init_logger(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='default.log',
                            filemode='w')
        global logger
        logger = logging.getLogger('posttracker')

        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # logger.addHandler(ch)
        logger.debug("logger initialized")

        # file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #
        #
        # fh = logging.FileHandler('1.log')
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)


def main():
    posttracker = PostTracker(cmdArgs=sys.argv[1:])
    result = posttracker.get_all_codes_with_status()
    logger.info(unicode(len(result)) + " post codes were processed successfully")
    output = open(posttracker.outputFileName, 'w')
    for codeItem in result:
        output.write(codeItem["code"] + ": " + codeItem["description"] + "\n")
        output.write(codeItem["status"].decode("utf-8") + "\n")
        output.write("---\n")

    output.close()


if __name__ == "__main__":
    main()