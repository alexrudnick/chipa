# for parallelism, go make -f <this file> -j <number of tasks to do
# simultaneously>

all: one two three

## QUECHUA

## GUARANI
# justwindow with stacking
one:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/justwindow_stacking.features

# justwindow with stacking and syntax
two:
	python3 clwsd_experiment.py --bitext ~/terere/bibletools/output/bible.es-gn --alignfn ~/terere/bibletools/output/bible.es-gn.align --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated --featurefn featuresets/justwindow_stacking_syntactic.features
