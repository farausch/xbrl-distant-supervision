from mimetypes import init
import spacy
import fasttext
from scipy import spatial
import config
from Levenshtein import distance

class SimilarityMeasure:

    def __init__(self):
        self.fasttext_model = None
        self.spacy_model = None

    def get_cosine_similarity_vec(self, vec1, vec2):
        return 1 - spatial.distance.cosine(vec1, vec2)

    def get_fasttext_similarity(self, str1, str2):
        if not self.fasttext_model:
            self.fasttext_model = fasttext.load_model(config.FASTTEXT_BIN_FILE)
        if len(str1.strip()) == 0 or len(str2.strip()) == 0:
            return -1
        for skip_token in [".", "%", "(", ")"]:
            if skip_token in str1:
                return -1
        return self.get_cosine_similarity_vec(self.fasttext_model.get_word_vector(str1), self.fasttext_model.get_word_vector(str2))

    def get_spacy_similarity(self, spacy_str1, spacy_str2):
        if not self.spacy_model:
            self.spacy_model = spacy.load(config.SPACY_MODEL_WITH_SIM_VECTORS)
        return spacy_str1.similarity(spacy_str2)
    
    def get_lev_similarity(self, str1, str2):
        sim = 1 - distance(str1, str2) / max(len(str1), len(str2))
        return sim