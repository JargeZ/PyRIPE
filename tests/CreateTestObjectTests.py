import unittest

from RipeApi import RipeApi
from models.Organisation import NewOrganisation


class CreateTestObjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = RipeApi(password='emptypassword', test_database=True, dry_run=False)

    def test_create_person(self):
        person = self.api.create_person(
            name="Pavel Khorikov",
            address="Pushkina string, Moscow, Russia",
            phone='+7 999 666 8228',
            email="jargez@ph3.ru",
            maintainer="TEST-NCC-HM-MNT"
        )
        self.assertIs(str, type(person.key))
        self.assertEqual("Pavel Khorikov", person.get_attr('person'))
        self.api.delete_person(nic_hdl=person.key)

    def test_delete_person(self):
        person = self.api.create_person(
            name="Pavel Khorikov",
            address="Pushkina string, Moscow, Russia",
            phone='+7 999 666 8228',
            email="jargez@ph3.ru",
            maintainer="TEST-NCC-HM-MNT"
        )
        deleted_person = self.api.delete_person(nic_hdl=person.key)
        self.assertEqual("Pavel Khorikov", deleted_person.get_attr('person'))

    def test_create_organisation(self):
        org = NewOrganisation(
            org_name="Test Organ",
            address="Pushkina string, Moscow, Russia",
            phone='+7 999 666 8228',
            e_mail="jargez@ph3.ru",
            maintainer="TEST-NCC-HM-MNT"
        )
        created = self.api.create_organization(org)
        self.assertIs(str, type(created.key))
        self.assertEqual("Test Organ", created.get_attr('org-name'))

        deleted = self.api.delete_organisation(organisation=created.key)
        self.assertEqual(created.key, deleted.key)
        self.assertEqual("Test Organ", deleted.get_attr('org-name'))




if __name__ == '__main__':
    unittest.main()
