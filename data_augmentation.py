from io_helper import IOHelper
import json
import config

ioh = IOHelper()

def get_xbrl_label_dict():
    with open(config.LABEL_RESOLUTION_KV, 'r') as f:
        data = json.load(f)
    return data

def is_number(string):
    string = string.replace(".", "").replace(",", ".")
    try:
        float(string)
        return True
    except ValueError:
        return False

def replace_entities(token_arr_freeze, annotation_arr_freeze, old_entity, new_entity, new_string):
    token_arr = [token for token in token_arr_freeze]
    annotation_arr = [annotation for annotation in annotation_arr_freeze]
    new_tokens = []
    new_annotations = []
    k = 0
    while k < len(token_arr) - 1:
        if annotation_arr[k] == old_entity and annotation_arr[k + 1] == old_entity:
            del annotation_arr[k]
            del token_arr[k]
        else:
            k += 1
    for i in range(len(token_arr)):
        if annotation_arr[i] == old_entity:
            if not is_number(token_arr[i]):
                for j in range(len(new_string.split(" "))):
                    new_tokens.append(new_string.split(" ")[j])
                    new_annotations.append(new_entity)
            else:
                new_tokens.append(token_arr[i])
                new_annotations.append(new_entity)
        else:
            new_tokens.append(token_arr[i])
            new_annotations.append(annotation_arr[i])
    return new_tokens, new_annotations

def set_new_xbrl_entity_idx(label_dict, val, plus):
    if val + plus >= len(label_dict):
        val -= len(label_dict)
    return val + plus

def augment_data(input_file, augment_steps_per_entity, multi_match_booster):
    xbrl_entity_idx = 0
    label_dict = get_xbrl_label_dict()
    e_keys = list(label_dict.keys())
    e_values = list(label_dict.values())
    ref, tokens, annotations = ioh.get_ground_truth_triplets(input_file)
    for ref, token_semic, annotation_semic in zip(ref, tokens, annotations):
        tks = token_semic.split(";")
        ans = annotation_semic.split(";")
        print(ref)
        print(str(tks).replace("[", "").replace("]", "").replace(", ", ";").replace("'", ""))
        print(str(ans).replace("[", "").replace("]", "").replace(", ", ";").replace("'", ""))
        if len(tks) == len(ans):
            for entity in set(ans):
                if entity != "0":
                    iteration_booster = multi_match_booster if len(set(ans)) > 2 else 0
                    for augment_step in range(augment_steps_per_entity + iteration_booster):
                        xbrl_entity_idx = set_new_xbrl_entity_idx(label_dict, xbrl_entity_idx, 1)
                        for val in e_values[xbrl_entity_idx]:
                            if not val.startswith("davon") and not e_keys[xbrl_entity_idx] in set(ans):
                                new_tokens, new_annotations = replace_entities(tks, ans, entity, e_keys[xbrl_entity_idx], val)
                                print(ref)
                                print(str(new_tokens).replace("[", "").replace("]", "").replace(", ", ";").replace("'", ""))
                                print(str(new_annotations).replace("[", "").replace("]", "").replace(", ", ";").replace("'", ""))

augment_data(config.AUGMENT_FILE, config.AUGMENT_STEPS, config.AUGMENT_MULTI_MATCH_BOOSTER)