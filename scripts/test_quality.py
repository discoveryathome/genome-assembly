import copy
import unittest
from quality import FIELDS, quality_gate, exact_gate

class Gates(unittest.TestCase):
    def setUp(self):
        self.good = {key: 0.0 for key in FIELDS}
        self.good.update(genome_fraction=100.0, duplication_ratio=1.0,
                         n50=250000.0, ng50=250000.0, nga50=250000.0,
                         contigs=1.0, total_length=250000.0)

    def test_known_equal_passes(self):
        self.assertEqual([], quality_gate(self.good, self.good))
        self.assertTrue(exact_gate({'gfa': 'abc', 'fasta': 'def'}, {'gfa': 'abc', 'fasta': 'def'}))

    def test_wrong_candidates_rejected(self):
        for key, value in [('misassemblies', 1), ('local_misassemblies', 1),
                           ('genome_fraction', 99.99), ('nga50', 249999),
                           ('n50', 249999), ('ng50', 249999), ('contigs', 2),
                           ('mismatches_per_100kb', .01), ('indels_per_100kb', .01),
                           ('duplication_ratio', 1.01), ('unaligned_length', 1)]:
            with self.subTest(key=key):
                bad = copy.deepcopy(self.good)
                bad[key] = value
                self.assertTrue(quality_gate(self.good, bad))
        self.assertFalse(exact_gate({'gfa': 'abc'}, {'gfa': 'bad'}))

    def test_missing_and_nan_fail_closed(self):
        bad = dict(self.good)
        del bad['misassemblies']
        with self.assertRaises(ValueError):
            quality_gate(self.good, bad)
        bad = dict(self.good, nga50=float('nan'))
        with self.assertRaises(ValueError):
            quality_gate(self.good, bad)

if __name__ == '__main__':
    unittest.main()
