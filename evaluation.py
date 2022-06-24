import spacy
import logging
import config
import spacy
import numpy as np
from datetime import datetime
from spacy.tokens import Doc
from io_helper import IOHelper
from xbrl_extraction import XbrlExtraction
from xml_extraction import XmlExtraction

xbrl_extr = XbrlExtraction()
xml_extr = XmlExtraction()
io_helper = IOHelper()

def evaluate_annotations(truth_xbrl_files, truth_tokens, truth_annotations):
    print("entity type;minimum digit start equal;similarity threshold;TP;TN;FP;FN;precision;recall")
    nlp_trf = spacy.load(config.SPACY_MODEL_TRANSFORMER)
    for min_digit in range(config.EVAL_MIN_DIGIT_LENGTH_EQUAL_START, config.EVAL_MIN_DIGIT_LENGTH_EQUAL_STOP):
        for min_sim in np.arange(0.5, 1.1, 0.1):
            val_tp, val_tn, val_fp, val_fn = 0, 0, 0, 0
            entity_tp, entity_tn, entity_fp, entity_fn = 0, 0, 0, 0
            for i in range(len(truth_xbrl_files)):
                sentence_tokens = [token for token in truth_tokens[i].split(";")]
                sentence_tokens = [sentence_token for sentence_token in sentence_tokens if sentence_token != ""]
                sentence = Doc(nlp_trf.vocab, words=sentence_tokens)
                entity_value_dict = xbrl_extr.get_entity_value_dict(truth_xbrl_files[i])
                predicted_annotations_values = xml_extr.get_financial_value_annotations(sentence, entity_value_dict, min_digit)
                predicted_annotations_entities = xml_extr.get_financial_entity_annotations(sentence, [entity for entity in entity_value_dict if entity in predicted_annotations_values], config.MAX_NGRAM_LENGTH, min_sim, config.STRING_COMPARISON_METHOD)
                predicted_annotations_entities, predicted_annotations_values = multi_match_barrier(predicted_annotations_entities, predicted_annotations_values)
                token_counter = 0
                for predicted_annotation_value, predicted_annotation_entity, truth_annotation in zip(predicted_annotations_values, predicted_annotations_entities, truth_annotations[i].split(";")):
                    if xml_extr.is_number(sentence_tokens[token_counter]):
                        if predicted_annotation_value != 0 and truth_annotation != "0":
                            if predicted_annotation_value.startswith(truth_annotation) or truth_annotation.startswith(predicted_annotation_value):
                                val_tp += 1
                            else:
                                val_fp += 1
                        elif predicted_annotation_value == 0 and truth_annotation == "0":
                            val_tn += 1
                        elif predicted_annotation_value != 0 and truth_annotation == "0":
                            val_fp += 1
                        elif predicted_annotation_value == 0 and truth_annotation != "0":
                            val_fn += 1
                    else:
                        if predicted_annotation_entity != 0 and truth_annotation != "0":
                            if predicted_annotation_entity.startswith(truth_annotation) or truth_annotation.startswith(predicted_annotation_entity):
                                entity_tp += 1
                            else:
                                entity_fp += 1
                        elif predicted_annotation_entity == 0 and truth_annotation == "0":
                            entity_tn += 1
                        elif predicted_annotation_entity != 0 and truth_annotation == "0":
                            entity_fp += 1
                        elif predicted_annotation_entity == 0 and truth_annotation != "0":
                            entity_fn += 1
                    token_counter += 1
            print("Numeric;", min_digit, ";", min_sim, ";", val_tp, ";", val_tn, ";", val_fp, ";", val_fn, ";", val_tp / (val_tp + val_fp), ";", val_tp / (val_tp + val_fn))
            print("Text;", min_digit, ";", min_sim, ";", entity_tp, ";", entity_tn, ";", entity_fp, ";", entity_fn, ";", entity_tp / (entity_tp + entity_fp), ";", entity_tp / (entity_tp + entity_fn))

def multi_match_barrier(entity_annotations, value_annotations):
    entity_annotations = [entity_annotation if entity_annotation in value_annotations else 0 for entity_annotation in entity_annotations]
    value_annotations = [value_annotation if value_annotation in entity_annotations else 0 for value_annotation in value_annotations]
    return entity_annotations, value_annotations

xbrl_files, tokens, annotations = io_helper.get_ground_truth_triplets(config.EVAL_GROUND_TRUTH_FILE)
evaluate_annotations(xbrl_files, tokens, annotations)