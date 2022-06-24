import json
from io_helper import IOHelper
import config

ioh = IOHelper()

def is_numeric(string):
    string = string.replace(".", "").replace(",", ".")
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_virtual_index_val(arr, idx):
    if idx == -1:
        return "0"
    elif idx == len(arr):
        return "0"
    else:
        return arr[idx]

def convert_to_conll(refs, tokens, annotations):
    formatted_sentences = []
    for i in range(len(refs)):
        sentence = {}
        entities = []
        relations = []
        token_list = tokens[i].split(";")
        annotation_list = annotations[i].split(";")
        
        current_pointer = -1
        for a in range(len(annotation_list) + 1):
            if get_virtual_index_val(annotation_list, a) != "0" and get_virtual_index_val(annotation_list, a - 1) == "0":
                current_pointer = a
            elif get_virtual_index_val(annotation_list, a) == "0" and get_virtual_index_val(annotation_list, a - 1) != "0":
                entity = {}
                entity["type"] = "financial_value" if is_numeric(get_virtual_index_val(token_list, a - 1)) else "financial_entity"
                entity["xbrl_id"] = get_virtual_index_val(annotation_list, a - 1)
                entity["start"] = current_pointer
                entity["end"] = a
                entities.append(entity)
        for ea in range(len(entities)):
            for eb in range(len(entities)):
                if entities[ea]["xbrl_id"] == entities[eb]["xbrl_id"] and entities[ea]["type"] == "financial_entity" and ea != eb:
                    relation = {}
                    relation["type"] = "has_value"
                    relation["head"] = ea
                    relation["tail"] = eb
                    relations.append(relation)

        sentence["tokens"] = token_list
        sentence["entities"] = entities
        sentence["relations"] = relations
        sentence["orig_id"] = refs[i]
        formatted_sentences.append(sentence)
    with open("conll.json", "w", encoding="utf8") as f:
        json.dump(formatted_sentences, f, ensure_ascii=False, indent=4)

r, t, a = ioh.get_ground_truth_triplets(config.CONLL_INPUT_FILE)
convert_to_conll(r, t, a)