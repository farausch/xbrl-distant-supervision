import logging
import config
import os
from io_helper import IOHelper
from xbrl_extraction import XbrlExtraction
from entity_resolution import EntityResolution
from xml_extraction import XmlExtraction

ent_res = EntityResolution(config.LABEL_RESOLUTION_DIR)
xbrl_extr = XbrlExtraction()
xml_extr = XmlExtraction()
io_helper = IOHelper()

# Extract sentences from financial statements where both a financial value and financial entity are found
def annotate_financial_reports(xbrl_files):
    for xbrl_file in xbrl_files:
        xml_file = xbrl_file.replace(".xbrl", ".xml")
        if os.path.isfile(xml_file):
            entity_value_dict = xbrl_extr.get_entity_value_dict(xbrl_file)
            file_sentences = xml_extr.get_all_sentences(xml_file)
            for sentence in file_sentences:
                # Extract financial values
                financial_value_annotations = xml_extr.get_financial_value_annotations(sentence, entity_value_dict, config.MIN_DIGIT_LENGTH_EQUAL)
                # Extract financial entities
                financial_entity_annotations = xml_extr.get_financial_entity_annotations(sentence, [entity for entity in entity_value_dict if entity in financial_value_annotations], config.MAX_NGRAM_LENGTH, config.STRING_COMPARISON_THRESHOLD, config.STRING_COMPARISON_METHOD)
                # Remove financial value annotations where not financial entity was found (multi-match barrier)
                financial_value_annotations = [value_annotation if value_annotation in financial_entity_annotations else 0 for value_annotation in financial_value_annotations]
                if len(financial_value_annotations) > 0 and financial_value_annotations.count(0) != len(financial_value_annotations):
                    print(xbrl_file)
                    print(str([token.text for token in sentence]).replace("[", "").replace("]", "").replace(", ", ";").replace("'", ""))
                    print(str(merge_annotations(financial_value_annotations, financial_entity_annotations)).replace("[", "").replace("]", "").replace(", ", ";").replace("'", ""))

def merge_annotations(arr1, arr2):
    merged = []
    for a, b in zip(arr1, arr2):
        merged.append(a if a != 0 else b)
    return merged

logging.getLogger().setLevel(logging.DEBUG)
xbrl_files = io_helper.get_all_financial_statement_files(config.BASE_DIR_FINANCIAL_REPORTS, ".xbrl")
annotate_financial_reports(xbrl_files)