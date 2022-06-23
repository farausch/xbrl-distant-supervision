# Entity resolution
LABEL_RESOLUTION_KV = "data/entity_label_dict_customized.json"
LABEL_RESOLUTION_DIR = "data/taxonomies/label-files/"
LABEL_PREFIX_ID_SEPARATOR = "_"

# XBRL extraction
BASE_DIR_FINANCIAL_REPORTS = "data/financial-statements/"
BASE_DIR_TAXONOMY = "german-gaap-taxonomy-v6.2-2018-04-01/"
XBRL_PREFIX_ID_SEPARATOR = ":"
PREFIX_GAAP = "de-gaap-ci"
FINANCIAL_VALUE_INDICATORS = ["TEUR", "EUR", "€", "Euro"]

# BeautifulSoup parsers
BS_PARSER_XBRL = "lxml"
BS_PARSER_XML = "lxml-xml"

# Language models
FASTTEXT_BIN_FILE = "data/cc.de.300.bin"
SPACY_MODEL_TRANSFORMER = "de_dep_news_trf"
SPACY_MODEL_WITH_SIM_VECTORS = "de_core_news_lg"

# Extraction parameters
STRING_COMPARISON_METHODS = ["levenshtein", "fasttext", "spacy"]
STRING_COMPARISON_METHOD = STRING_COMPARISON_METHODS[0]
STRING_COMPARISON_THRESHOLD = 0.8
MIN_DIGIT_LENGTH_EQUAL = 1
MAX_NGRAM_LENGTH = 4