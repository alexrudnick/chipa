#! /usr/bin/python3

import fileinput
import sys

import freeling

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local";
DATA = FREELINGDIR+"/share/freeling/";
LANG="es";
freeling.util_init_locale("default");

# create options set for maco analyzer. Default values are Ok, except for data files.
op = freeling.maco_options("es")
op.set_active_modules(0,1,1,1,1,1,1,1,1,1)
op.set_data_files("",DATA+LANG+"/locucions.dat", DATA+LANG+"/quantities.dat", 
                  DATA+LANG+"/afixos.dat", DATA+LANG+"/probabilitats.dat", 
                  DATA+LANG+"/dicc.src", DATA+LANG+"/np.dat",  
                  DATA+"common/punct.dat")

# create analyzers
tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
sp=freeling.splitter(DATA+LANG+"/splitter.dat")
mf=freeling.maco(op)
tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",1,2);
#sen=freeling.senses(DATA+LANG+"/senses.dat");
#parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
#dep=freeling.dep_txala(DATA+LANG+"/dep/dependences.dat", parser.get_start_symbol());

def preprocess(line):
    l = tk.tokenize(line)
    ls = sp.split(l,0)
    ls = mf.analyze(ls)
    ls = tg.analyze(ls)
    ## could add other analysis here.
    return ls

def main():
    for line in fileinput.input():
        ls = preprocess(line)
        for s in ls:
            ws = s.get_words()
            for w in ws:
                print("{0} {1} {2}".format(
                    w.get_form(), w.get_lemma(), w.get_tag()))
        print()

if __name__ == "__main__": main()
