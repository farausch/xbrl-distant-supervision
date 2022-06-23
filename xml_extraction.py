from __future__ import annotations
from re import X
from tkinter import N
import config
import spacy
from bs4 import BeautifulSoup
from entity_resolution import EntityResolution
from similarity_measure import SimilarityMeasure

class XmlExtraction:

    def __init__(self):
        self.nlp_trf = spacy.load(config.SPACY_MODEL_TRANSFORMER)
        self.entity_resolution = EntityResolution(config.LABEL_RESOLUTION_DIR)
        self.sim_measure = SimilarityMeasure()

    def is_number(self, string):
        string = string.replace(".", "").replace(",", ".")
        try:
            float(string)
            return True
        except ValueError:
            return False

    def sentence_has_financial_value(self, spacy_sentence):
        tokens = [token.text for token in spacy_sentence]
        for indicator in config.FINANCIAL_VALUE_INDICATORS:
            if indicator in tokens:
                return True
        return False

    def get_xbrl_entity_for_num_token_fuzzy_match(self, token, xbrl_key_value_dict, min_len):
        token = token.replace(".", "").replace(",", "")
        if len(token) < min_len:
            return 0
        for token in [int(token), int(token) - 1]:
            for xbrl_entity, xbrl_number in xbrl_key_value_dict.items():
                if xbrl_number.replace(".", "").startswith(str(token)):
                    return xbrl_entity
        return 0
    
    def get_all_sentences(self, xml_file):
        all_sentences = []
        with open(xml_file) as xml:
            soup = BeautifulSoup(xml, config.BS_PARSER_XML)
        for tag in soup.find_all("A"):
            section = tag.text.replace("\n", " ")
            spacy_section = self.nlp_trf(section)
            for sentence in spacy_section.sents:
                all_sentences.append(sentence)
        return all_sentences

    def get_financial_value_annotations(self, spacy_sentence, xbrl_key_value_dict, min_len):
        annotations = []
        tokens = [token.text for token in spacy_sentence]
        if self.sentence_has_financial_value(spacy_sentence):
            for token in tokens:
                if self.is_number(token):
                    annotation = self.get_xbrl_entity_for_num_token_fuzzy_match(token, xbrl_key_value_dict, min_len)
                    annotations.append(annotation)
                else:
                    annotations.append(0)
        return annotations

    def get_ngrams(self, tokens, max_len):
        return [tokens[i:i + max_len] for i in range(len(tokens) - max_len + 1)]

    def get_financial_entity_annotations(self, spacy_sentence, expected_entities, max_ngram, sim_threshold, comparison_method):
        annotations = [0] * len(spacy_sentence)
        entity_label_dict = {entity: self.entity_resolution.get_label_text(entity) for entity in expected_entities}
        entity_max_sim_dict = {entity: 0 for entity in expected_entities}
        for i in range(1, max_ngram + 1):
            for j in range(len(spacy_sentence) - i + 1):
                spacy_candidate_span = self.nlp_trf(spacy_sentence[j:j + i].text)
                for entity, labels in entity_label_dict.items():
                    for label in labels:
                        spacy_label = self.nlp_trf(label)
                        if comparison_method == "levenshtein":
                            sim = self.sim_measure.get_lev_similarity(spacy_sentence[j:j + i].text, label)
                        elif comparison_method == "fasttext":
                            sim = self.sim_measure.get_fasttext_similarity(spacy_sentence[j:j + i].text, label)
                        elif comparison_method == "spacy":
                            sim = self.sim_measure.get_spacy_similarity(spacy_candidate_span, spacy_label)
                        else:
                            raise ValueError("Unknown comparison method: " + comparison_method)
                        if sim >= sim_threshold and sim > entity_max_sim_dict[entity]:
                            entity_max_sim_dict[entity] = sim
                            for k in range(len(annotations)):
                                if annotations[k] == entity:
                                    annotations[k] = 0
                            for l in range(j, j + i):
                                annotations[l] = entity
        return annotations