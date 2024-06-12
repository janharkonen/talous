from context import talous_module
from talous_module.helper_functions import get_cur

import unittest

class TestDataTransformation(unittest.TestCase):
    def test_get_cur(self):
        self.assertEqual(get_cur('EUR','ATA'), 'ATA')

    def test_get_cur2(self):
        self.assertEqual('ATA', 'ATA')

if __name__ == '__main__':
    unittest.main()