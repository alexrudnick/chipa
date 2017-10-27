# for parallelism, go make -f <this file> -j <number of tasks to do
# simultaneously>

all: one two three four

## QUECHUA

## QUECHUA SURFACE
one:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-qu --alignfn ~/terere/bibletools/output/bible.es-qu.align --annotatedfn ~/chipa/src/annotated/bible.es-qu.source.annotated --featurefn featuresets/doc2vec_window_200.features

two:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-qu --alignfn ~/terere/bibletools/output/bible.es-qu.align --annotatedfn ~/chipa/src/annotated/bible.es-qu.source.annotated --featurefn featuresets/doc2vec_window_400.features

## GUARANI
## GUARANI SURFACE
three:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/doc2vec_window_200.features

four:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/doc2vec_window_400.features
