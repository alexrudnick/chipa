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
            "one\tone\tbrown_bible=0001",
            "two\ttwo\tbrown_bible=0010",
            "three\tthree\tbrown_bible=0011",
            "four\tfour\tbrown_bible=0100",
            "five\tfive\tbrown_bible=0101",
            "six\tsix\tbrown_bible=0110",
            "seven\tseven\tbrown_bible=0111",
            "eight\tsevent\tbrown_bible=1000",
            ".\t.\tbrown_bible=0000"
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

    def test_brown_bag_bible(self):
        feats = features.brown_bag_bible(self.tagged_sent, self.annotated[0], 0)
        self.assertIn("brown_bag_bible_complete(0000)", feats)
        self.assertIn("brown_bag_bible_complete(1000)", feats)
        self.assertIn("brown_bag_bible_0(1)", feats)
        self.assertIn("brown_bag_bible_0(0)", feats)
        self.assertIn("brown_bag_bible_1(00)", feats)

    def test_brown_window_bible(self):
        feats = features.brown_window_bible(self.tagged_sent,
                                            self.annotated[0],
                                            0)
        self.assertNotIn("brown_window_bible_complete(0000)", feats)
        self.assertIn("brown_window_bible_complete(0010)", feats)
        self.assertIn("brown_window_bible_complete(0011)", feats)

        feats = features.brown_window_bible(self.tagged_sent,
                                            self.annotated[0],
                                            8)
        self.assertIn("brown_window_bible_complete(1000)", feats)
        self.assertNotIn("brown_window_bible_complete(0000)", feats)
        self.assertNotIn("brown_window_bible_complete(0001)", feats)

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
        self.assertIn("brown_bag_europarl_complete(NONE)", feats)


        feats = features.brown_bag_europarl(self.tagged_sent,
                                            self.annotated_europarl[0],
                                            0)
        self.assertNotIn("brown_bag_europarl_complete(NONE)", feats)
        self.assertIn("brown_bag_europarl_complete(0000)", feats)

    def test_brown_window_europarl(self):
        feats = features.brown_window_europarl(self.tagged_sent,
                                               self.annotated_europarl[0],
                                               2)
        self.assertIn("brown_window_europarl_complete(0001)", feats)
        self.assertIn("brown_window_europarl_0(0)", feats)

if __name__ == '__main__':
    unittest.main()
