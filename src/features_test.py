import unittest
import random

import features
import annotated_corpus

class TestFeatures(unittest.TestCase):

    def setUp(self):
        sent_en = "one two three four five six seven eight ."
        sent_es = "uno dos tres quatro cinco seis siete ocho ."
        self.tagged_sent = list(zip(sent_en.split(), sent_es.split()))

        lines = [
            "one\tone\tbrown_wikipedia=0001",
            "two\ttwo\tbrown_wikipedia=0010",
            "three\tthree\tbrown_wikipedia=0011",
            "four\tfour\tbrown_wikipedia=0100",
            "five\tfive\tbrown_wikipedia=0101",
            "six\tsix\tbrown_wikipedia=0110",
            "seven\tseven\tbrown_wikipedia=0111",
            "eight\teight\tbrown_wikipedia=1000",
            ".\t.\tbrown_wikipedia=0000"
        ]
        self.annotated = annotated_corpus.load_corpus_from_lines(lines)

        lines = [
            "one\tone\tbrown_europarl=0001",
            "two\ttwo\tbrown_europarl=0010",
            "three\tthree\tbrown_europarl=0011",
            "four\tfour\tbrown_europarl=0100",
            "five\tfive\tbrown_europarl=0101",
            "six\tsix\tbrown_europarl=0110",
            "seven\tseven\tbrown_europarl=0111",
            "eight\tsevent\tbrown_europarl=1000",
            ".\t.\tbrown_europarl=0000"
        ]
        self.annotated_europarl = annotated_corpus.load_corpus_from_lines(lines)


        sent_en = "i kick the ball ."
        sent_es = "yo pateo la pelota ."
        self.tagged_sent2 = list(zip(sent_en.split(), sent_es.split()))
        lines = [
            "I\tI\ttag=PRON",
            "kick\tkicked\ttag=VERB",
            "the\tthe\ttag=DET",
            "ball\tball\ttag=NOUN",
            ".\t.\ttag=PUNCT",
        ]
        self.annotated_postags = annotated_corpus.load_corpus_from_lines(lines)

        sent_en = "i kick the ball ."
        sent_es = "yo pateo la pelota ."
        self.tagged_sent3 = list(zip(sent_en.split(), sent_es.split()))
        lines = [
            "I\tI\tword2vec_europarl=0.1_0.1",
            "kick\tkicked\tword2vec_europarl=0.2_0.2",
            "the\tthe\tword2vec_europarl=0.3_0.3",
            "ball\tball\tword2vec_europarl=0.4_0.4",
            ".\t.\tword2vec_europarl=0.5_0.5",
        ]
        self.annotated_word2vec = annotated_corpus.load_corpus_from_lines(lines)

        lines = [
            "I\tI\tword2vec_europarl=0.1_0.1",
            "kick\tkicked\tword2vec_europarl=0.2_0.2",
            "the\tthe\tpos=DET",
            "ball\tball\tword2vec_europarl=0.4_0.4",
            ".\t.\tword2vec_europarl=0.5_0.5",
        ]
        self.annotated_word2vec_missing = \
            annotated_corpus.load_corpus_from_lines(lines)

        lines = [
            "I\tI\tpos=foo",
            "kick\tkicked\tpos=foo",
            "the\tthe\tpos=foo",
            "ball\tball\tpos=foo",
            ".\t.\tpos=foo",
        ]
        self.annotated_word2vec_missing_all = \
            annotated_corpus.load_corpus_from_lines(lines)

        lines = [
            "the\tThe\tpos=foo",
            "quick\tquick\tpos=foo",
            "brown\tbrown\tpos=foo",
            "fox\tfox\tpos=foo",
            "jump\tjumped\tpos=foo",
            "over\tover\tpos=foo",
            "the\tthe\tpos=foo",
            "lazy\tlazy\tpos=foo",
            "sleep\tsleeping\tpos=foo",
            "dog\tdog\tpos=foo",
            ".\t.\tpos=foo",
        ]
        self.annotated_quickbrown = \
            annotated_corpus.load_corpus_from_lines(lines)
        sent_en = "the quick brown fox jump over the lazy sleeping dog ."
        sent_es = "the quick brown fox jump over the lazy sleeping dog ."
        self.tagged_sent3 = list(zip(sent_en.split(), sent_es.split()))

        sent_es = "estación"
        sent_eo = "sezono"
        self.tagged_sent_stacking = list(zip(sent_es.split(), sent_eo.split()))
        lines = [
            "estación\testación\tpos=foo\t" +
            "stack_default_esen=season\t" +
            "stack_default_esfr=saison\t" +
            "stack_default_esde=Saison"
        ]
        self.annotated_stacking = \
            annotated_corpus.load_corpus_from_lines(lines)

    def test_bagofwords(self):
        feats = features.bagofwords(self.tagged_sent3,
                                    self.annotated_quickbrown[0],
                                    0)
        self.assertIn("cw(the)", feats)
        self.assertEqual(feats["cw(the)"], 2)

    def test_window(self):
        feats = features.window(self.tagged_sent, self.annotated[0], 0)
        self.assertNotIn("w(one)", feats)
        self.assertIn("w(two)", feats)
        self.assertIn("w(three)", feats)
        self.assertIn("w(four)", feats)

        feats = features.window(self.tagged_sent, self.annotated[0], 1)
        self.assertIn("w(one)", feats)
        self.assertNotIn("w(two)", feats)
        self.assertIn("w(three)", feats)
        self.assertIn("w(four)", feats)
        self.assertIn("w(five)", feats)

    def test_brown_bag_wikipedia(self):
        feats = features.brown_bag_wikipedia(self.tagged_sent, self.annotated[0], 0)
        self.assertIn("brown_bag_wikipedia(0000)", feats)
        self.assertIn("brown_bag_wikipedia(1000)", feats)
        self.assertIn("brown_bag_wikipedia_4(0100)", feats)
        self.assertIn("brown_bag_wikipedia_4(0111)", feats)
        self.assertIn("brown_bag_wikipedia_4(0010)", feats)
        self.assertIn("brown_bag_wikipedia_10(0010)", feats)

    def test_brown_window_wikipedia(self):
        feats = features.brown_window_wikipedia(self.tagged_sent,
                                            self.annotated[0],
                                            0)
        self.assertNotIn("brown_window_wikipedia(0000)", feats)
        self.assertIn("brown_window_wikipedia(0001)", feats)
        self.assertIn("brown_window_wikipedia(0010)", feats)
        self.assertIn("brown_window_wikipedia(0011)", feats)

        feats = features.brown_window_wikipedia(self.tagged_sent,
                                            self.annotated[0],
                                            8)
        self.assertIn("brown_window_wikipedia(1000)", feats)
        self.assertIn("brown_window_wikipedia(0000)", feats)
        self.assertNotIn("brown_window_wikipedia(0001)", feats)

    def test_window_indices(self):
        indices = features.window_indices(0, 1, 2)
        self.assertEqual(indices, [1])

        indices = features.window_indices(0, 5, 2)
        self.assertEqual(indices, [1])

        indices = features.window_indices(0, 2, 3)
        self.assertEqual(indices, [1, 2])

        indices = features.window_indices(4, 5, 10)
        self.assertEqual(indices, [0, 1, 2, 3, 5, 6, 7, 8, 9])

    def test_brown_bag_europarl(self):
        ## No europarl annotations for this sentence!
        feats = features.brown_bag_europarl(self.tagged_sent,
                                            self.annotated[0],
                                            0)
        self.assertEqual(feats, {})

        feats = features.brown_bag_europarl(self.tagged_sent,
                                            self.annotated_europarl[0],
                                            0)
        self.assertNotIn("brown_bag_europarl(NONE)", feats)
        self.assertIn("brown_bag_europarl(0000)", feats)

    def test_brown_window_europarl(self):
        feats = features.brown_window_europarl(self.tagged_sent,
                                               self.annotated_europarl[0],
                                               2)
        self.assertIn("brown_window_europarl(0001)", feats)
        self.assertIn("brown_window_europarl_4(0001)", feats)

    def test_flat_brown_window_europarl(self):
        feats = features.flat_brown_window_europarl(self.tagged_sent,
                                                    self.annotated_europarl[0],
                                                    2)
        self.assertIn("fwe(0001)", feats)

    def test_flat_brown_window_wikipedia(self):
        feats = features.flat_brown_window_wikipedia(self.tagged_sent,
                                                     self.annotated[0],
                                                     2)
        self.assertIn("fww(0001)", feats)

    def test_brown_variations(self):
        variations = features.brown_variations("foo", "11111111")
        self.assertIn("foo(11111111)", variations)
        self.assertIn("foo_4(1111)", variations)
        self.assertIn("foo_6(111111)", variations)

    def test_postag(self):
        feats = features.postag(self.tagged_sent2,
                                self.annotated_postags[0],
                                2)
        self.assertEqual({"postag(DET)": True}, feats)

    def test_postag_left(self):
        feats = features.postag_left(self.tagged_sent2,
                                     self.annotated_postags[0],
                                     2)
        self.assertEqual({"postag_left(VERB)": True}, feats)

    def test_postag_right(self):
        feats = features.postag_right(self.tagged_sent2,
                                      self.annotated_postags[0],
                                      2)
        self.assertEqual({"postag_right(NOUN)": True}, feats)

    def test_surfaceform(self):
        feats = features.surfaceform(self.tagged_sent2,
                                     self.annotated_postags[0],
                                     0)
        self.assertEqual({"surfaceform(I)": True}, feats)

        feats = features.surfaceform(self.tagged_sent2,
                                     self.annotated_postags[0],
                                     1)
        self.assertEqual({"surfaceform(kicked)": True}, feats)

    def test_stacking(self):
        feats = features.stacking_de(self.tagged_sent_stacking,
                                     self.annotated_stacking[0],
                                     0)
        self.assertEqual({"stacking_de(Saison)": True}, feats)

        feats = features.stacking_en(self.tagged_sent_stacking,
                                     self.annotated_stacking[0],
                                     0)
        self.assertEqual({"stacking_en(season)": True}, feats)

        feats = features.stacking_fr(self.tagged_sent_stacking,
                                     self.annotated_stacking[0],
                                     0)
        self.assertEqual({"stacking_fr(saison)": True}, feats)

if __name__ == '__main__':
    unittest.main()
