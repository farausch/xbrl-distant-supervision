import config
import re
from bs4 import BeautifulSoup

class XbrlExtraction:

    def get_entity_value_dict(self, xbrl_file):
        entity_value_dict = {}
        with open(xbrl_file) as xbrl:
            soup = BeautifulSoup(xbrl, config.BS_PARSER_XBRL)
        for tag in soup.find_all(re.compile("^" + config.PREFIX_GAAP)):
            entity_value_dict[tag.name] = tag.text
        return entity_value_dict