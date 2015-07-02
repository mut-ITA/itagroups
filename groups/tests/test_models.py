from django.test import TestCase
from django.core.exceptions import ValidationError

from groups.models import Group, User
from groups.HelperMethods.tests import create_sample_database, create_sample_user_database

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

	@skip
	def test_get_absolute_url(self):
		create_sample_database()
		group = Group.objects.all()[0]
		self.assertEqual(group.get_absolute_url(), '/groups/%s/' % (group.alias))

class UserModelTest(TestCase):

	def test_saving_and_retrieving_users(self):
		create_sample_user_database()

		saved_users = User.objects.all()
		self.assertEqual(saved_users.count(), 2)

		first_saved_user = saved_users[0]
		second_saved_user = saved_users[1]
		self.assertEqual(first_saved_user.access_token, 'Username1')
		self.assertEqual(second_saved_user.access_token, 'Username2')

	def test_cannot_save_empty_user(self):
		user = User(access_token = '', apelido = '', turma = '')
		with self.assertRaises(ValidationError):
			user.save()
			user.full_clean()

	def test_get_absolute_url(self):
		user = User.objects.create()
		self.assertEqual(user.get_absolute_url(), '/user/%s/' % (user.id))


class UserGroupRelationTest(TestCase):

	def test_group_has_multiples_users(self):
		create_sample_database()
		create_sample_user_database()

		saved_users = User.objects.all()

		first_saved_user = saved_users[0]
		second_saved_user = saved_users[1]

		saved_groups = Group.objects.all()

		first_saved_group = saved_groups[0]
		second_saved_group = saved_groups[1]

		first_saved_user.groups.add(first_saved_group)

		second_saved_user.groups.add(first_saved_group)

		self.assertEqual(first_saved_group.user_set.all().count(), 2)

	def test_user_has_multiples_groups(self):
		create_sample_database()
		create_sample_user_database()

		saved_users = User.objects.all()

		first_saved_user = saved_users[0]
		second_saved_user = saved_users[1]

		saved_groups = Group.objects.all()

		first_saved_group = saved_groups[0]
		second_saved_group = saved_groups[1]

		first_saved_user.groups.add(first_saved_group)

		first_saved_user.groups.add(second_saved_group)

		self.assertEqual(first_saved_user.groups.all().count(), 2)
