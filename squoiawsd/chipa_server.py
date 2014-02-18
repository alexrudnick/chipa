#!/usr/bin/env python3

import learn
import brownclusters

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

def label_sentence(sentence):
    """Take a list of lemmas and return a list of target-language lemmas, which
    might be the <untranslated> token."""
    print("LABELING A SENTENCE HANG ON.")
    lemmas = [tup[2] for tup in sentence]
    answers = learn.prob_disambiguate_words(lemmas)
    print("sent to client:", answers)
    return answers

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def _dispatch(self, method, params):
        try: 
            return self.server.funcs[method](*params)
        except:
            import traceback
            traceback.print_exc()
            raise

def main():
    parser = learn.get_argparser()

    args = parser.parse_args()
    brownclusters.set_paths_file(args.clusterfn)
    triple_sentences = learn.load_bitext(args)
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    learn.set_examples(sl_sentences,tagged_sentences)

    # Create server
    server = SimpleXMLRPCServer(("localhost", 8000),
                                requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_function(label_sentence)
    print("SERVER IS NOW ON IT.")
    server.serve_forever()

if __name__ == "__main__": main()
