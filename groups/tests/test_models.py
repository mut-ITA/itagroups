from django.test import TestCase
from django.core.exceptions import ValidationError

from groups.models import Group
from groups.HelperMethods.tests import create_sample_database

class GroupModelTest(TestCase):

	def test_saving_and_retrieving_groups(self):
		create_sample_database()

		saved_groups = Group.objects.all()
		self.assertEqual(saved_groups.count(), 2)

		first_saved_group = saved_groups[0]
		second_saved_group = saved_groups[1]
		self.assertEqual(first_saved_group.name, 'Teh name')
		self.assertEqual(first_saved_group.alias, 'tehalias')
		self.assertEqual(first_saved_group.tags, 'Teh; tags')
		self.assertEqual(first_saved_group.description, 'Teh description')
		self.assertEqual(second_saved_group.name, 'Teh name2')

	def test_cannot_save_empty_group(self):
		group = Group(name = '', alias = '', tags = '', description = '')
		with self.assertRaises(ValidationError):
			group.save()
			group.full_clean()