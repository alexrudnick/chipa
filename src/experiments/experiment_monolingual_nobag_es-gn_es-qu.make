# for parallelism, go make -f <this file> -j <number of tasks to do
# simultaneously>

all: one two

## QUECHUA

## QUECHUA SURFACE
one:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-qu --alignfn ~/terere/bibletools/output/bible.es-qu.align --annotatedfn ~/chipa/src/annotated/bible.es-qu.source.annotated --featurefn featuresets/monolingual_nobag.features --embeddings /space/clustering/word2vec-spanish-wikipedia-200.skipgram --embedding_dim 200 

## GUARANI
## GUARANI SURFACE
two:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/monolingual_nobag.features --embeddings /space/clustering/word2vec-spanish-wikipedia-200.skipgram --embedding_dim 200 
