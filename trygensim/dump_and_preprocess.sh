FREELINGCONFIGDIR=/home/alex/terere/bibletools/freeling-config
WIKIPEDIA=/space/spanish-wikipedia/eswiki-latest-pages-articles-2016-07-19.xml.bz2

python3 dumpwikipedia.py $WIKIPEDIA ./eswiki.txt

analyze -f $FREELINGCONFIGDIR/es.cfg \
  < eswiki.txt \
  > eswiki.tagged

cut -f 1 -d " " < eswiki.tagged > eswiki.justwords

python3 joinsentences.py eswiki.justwords > eswiki.sentences
