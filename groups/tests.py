from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from groups.views import home_page
from groups.models import Group

# Create your tests here.

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)


class CreateGroupTest(TestCase):

	def test_create_group_form_can_save_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['group_name'] = 'New group name'
		request.POST['group_alias'] = 'Newgroupalias'
		request.POST['group_tags'] = 'New group tags'
		request.POST['group_description'] = 'New group description'

		response = home_page(request)

		self.assertIn('New group name', response.content.decode())
		self.assertIn('Newgroupalias', response.content.decode())
		self.assertIn('New group tags', response.content.decode())
		self.assertIn('New group description', response.content.decode())

		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/')

	def test_create_group_POST_save_to_db(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['group_name'] = 'New group name'
		request.POST['group_alias'] = 'Newgroupalias'
		request.POST['group_tags'] = 'New group tags'
		request.POST['group_description'] = 'New group description'

		response = home_page(request)

		self.assertEqual(Group.objects.count(), 1)
		new_group = Group.objects.first()
		self.assertEqual(new_group.name, 'New group name')
		self.assertEqual(new_group.alias, 'Newgroupalias')
		self.assertEqual(new_group.tags, 'New group tags')
		self.assertEqual(new_group.description, 'New group description')

class GroupModelTest(TestCase):

	def test_saving_and_retrieving_groups(self):
		first_group = Group()
		first_group.name = 'Teh name'
		first_group.alias = 'Tehalias'
		first_group.tags = 'Teh tags'
		first_group.description = 'Teh description' 
		first_group.save()

		second_group = Group()
		second_group.name = 'Teh name2'
		second_group.save()

		saved_groups = Group.objects.all()
		self.assertEqual(saved_groups.count(), 2)

		first_saved_group = saved_groups[0]
		second_saved_group = saved_groups[1]
		self.assertEqual(first_saved_group.name, 'Teh name')
		self.assertEqual(first_saved_group.alias, 'Tehalias')
		self.assertEqual(first_saved_group.tags, 'Teh tags')
		self.assertEqual(first_saved_group.description, 'Teh description')
		self.assertEqual(second_saved_group.name, 'Teh name2')