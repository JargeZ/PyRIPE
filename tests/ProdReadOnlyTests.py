import unittest

from RipeApi import RipeApi


class ProdReadOnlyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = RipeApi(password='', test_database=False)

    def test_get_inum(self):
        inum = self.api.get_inetnum('84.23.56.0 - 84.23.63.255')
        self.assertEqual(inum.primary_key.attribute[0].value, '84.23.56.0 - 84.23.63.255')

    def test_get_person(self):
        inum = self.api.get_person('AAB155-RIPE')
        self.assertEqual(inum.primary_key.attribute[0].value, 'AAB155-RIPE')


if __name__ == '__main__':
    unittest.main()
