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

### Run annotation

Run the distant supervision annotation algorithm and obtain annotated data triplets (file, tokens, annotations) after changing the config.py to your desired configuration:
```
python text_annotation.py > financial_sentences_annotated.csv
```

In data/financial-statements is one pair of XBRL and XML documents. Place your own financial statements as pairs of these in order to annotate them automatically. The algorithm iterates over each file in this folder. XBRL and XML files that belong together must have the same file name except the file extension. Please note that the annotation algorithm is resource intensive depending on the parameters (especially the maximum length of n-grams to create) and takes some time even for a little amount of files.

## Evaluation

Run evaluation for the distant supervision parameters configured in config.py:
```
python evaluation.py > evaluation.csv
```

The evaluation is stored to the file in csv format and can be processed further or imported to Excel.