FREELINGCONFIGDIR=/home/alex/terere/bibletools/freeling-config
WIKIPEDIA=/space/spanish-wikipedia/eswiki-latest-pages-articles-2016-07-19.xml.bz2

python3 dumpwikipedia.py $WIKIPEDIA ./eswiki.txt

analyze -f $FREELINGCONFIGDIR/es.cfg \
  < eswiki.txt \
  > eswiki.tagged
