import io
import subprocess
import sys

def call_freeling_on(fn):
    """Given a filename, run freeling on that file."""
    text = ""
    with open(fn) as infile:
        output = subprocess.check_output(
                    ["/usr/local/bin/analyze",
                     "-f",
                     "/home/alex/squoia_environment/squoia-read-only/FreeLingModules/squoia.cfg"],
                     stdin=infile)
        text = output.decode('utf-8')
    sentences = [line.strip().split("\n") for line in text.split("\n\n")]

    for sentence in sentences:
        for wordline in sentence:
            if not wordline: continue
            fields = wordline.split()
            lemma = fields[1]
            print(lemma, end=" ")
        print()

def main():
    fn = sys.argv[1]
    call_freeling_on(fn)

if __name__ == "__main__": main()
