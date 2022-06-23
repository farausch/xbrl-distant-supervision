# XBRL distant supervision

## Data annotation with distant supervision

### Setup
Install requirements:
```
pip install -r requirements.txt
```

Install required spaCy language models:
```
python -m spacy download de_core_news_lg
python -m spacy download de_dep_news_trf
```

If FastText vectors are used for string comparison, download FastText vectors (https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.et.300.bin.gz) and point to the file in config.py

Change config.py to your desired configuration.

Run the distant supervision annotation algorithm and obtain annotated data triplets (file, tokens, annotations):
```
python text_annotation.py > financial_sentences_annotated.txt
```

In data/financial-statements is one pair of XBRL and XML documents. Place your own financial statements as pairs of these in order to annotate them automatically. The algorithm iterates over each file in this folder. XBRL and XML files that belong together must have the same file name except the file extension.