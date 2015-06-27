from django.test import TestCase
from django.core.exceptions import ValidationError

from groups.models import Group, User
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

class UserModelTest(TestCase):

	def test_saving_and_retrieving_users(self):
		user1 = User.objects.create(access_token = 'Usuario', apelido = 'Guilhon', turma = 'T16')
		user2 = User.objects.create(access_token = 'Usuario2', apelido = 'Guilhon2', turma = 'T162')

		saved_users = User.objects.all()
		self.assertEqual(saved_users.count(), 2)

		first_saved_user = saved_users[0]
		second_saved_user = saved_users[1]
		self.assertEqual(first_saved_user.access_token, 'Usuario')
		self.assertEqual(second_saved_user.access_token, 'Usuario2')

	def test_cannot_save_empty_user(self):
		user = User(access_token = '', apelido = '', turma = '')
		with self.assertRaises(ValidationError):
			user.save()
			user.full_clean()