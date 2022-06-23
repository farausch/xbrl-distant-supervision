import json
from logging import log
import os
from nltk.util import pr
import config
import logging
from bs4 import BeautifulSoup

class EntityResolution:

    def __init__(self, label_file_dir):
        if os.path.exists(config.LABEL_RESOLUTION_KV):
            with open(config.LABEL_RESOLUTION_KV, "r") as f:
                self.entity_label_dict = json.load(f)
                self.stored_dict = True
        else:
            self.stored_dict = False
            self.label_soups = []
            label_files = os.listdir(label_file_dir)
            for label_file in label_files:
                if label_file.endswith(".xml"):
                    with open(label_file_dir + label_file) as label:
                        self.label_soups.append(BeautifulSoup(label, config.BS_PARSER_XBRL))

    def get_label_text(self, xbrl_id):
        if self.stored_dict:
            return self.entity_label_dict[xbrl_id]
        else:
            xbrl_id_converted = config.PREFIX_GAAP + config.LABEL_PREFIX_ID_SEPARATOR + xbrl_id.split(config.XBRL_PREFIX_ID_SEPARATOR)[1]
            labels = set()
            for soup in self.label_soups:
                for tag in soup.find_all(name="labelarc", attrs={"xlink:from": lambda x: x and x.lower()==xbrl_id_converted.lower()}):
                    label_tag = soup.find(attrs={"id": tag["xlink:to"]})
                    if not "documentation" in label_tag["xlink:role"]:
                        labels.add(label_tag.text)
            if len(labels) == 0:
                logging.warning("There was no plain text label found for: " + xbrl_id)
            return sorted(labels, key=len)