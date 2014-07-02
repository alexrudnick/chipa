#!/usr/bin/env python3


import unittest

import learn

class TestAlignment(unittest.TestCase):
    def setUp(self):
        pass

    def test_target_words_for_each_source_word(self):
        src = "four three two one".split()
        trg = "1 1 2 3 4".split()
        align = "0-4 1-3 2-2 3-1 3-0".split()
        twss = learn.target_words_for_each_source_word(src, trg, align)
        self.assertEqual(twss, ['4', '3', '2', '1 1'])

        src = "a b c d".split()
        trg = "a c1 b c2 d".split()
        align = "0-0 1-2 2-1 2-3 3-4".split()
        twss = learn.target_words_for_each_source_word(src, trg, align)
        self.assertEqual(twss, ['a', 'b', 'c1', 'd'])

if __name__ == '__main__':
    unittest.main()
