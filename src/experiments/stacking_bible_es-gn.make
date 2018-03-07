# for parallelism, go make -f <this file> -j <number of tasks to do
# simultaneously>

all: two three

## QUECHUA

## GUARANI
# only stacking
## one:
## 	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/only_stacking.features

# default + stacking
two:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/bible_stacking.features

# default + syntactic + stacking
three:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/bible_stacking_syntactic.features
