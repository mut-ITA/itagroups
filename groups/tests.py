from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from groups.views import home_page, search_groups
from groups.models import Group
from groups.HelperMethods.tests import create_sample_database, create_sample_POST_request

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
		request = create_sample_POST_request()

		response = home_page(request)

		self.assertIn('New group name', response.content.decode())
		self.assertIn('newgroupalias', response.content.decode())
		self.assertIn('New; group; tags', response.content.decode())
		self.assertIn('New group description', response.content.decode())

		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/')

	def test_create_group_POST_save_to_db(self):
		request = create_sample_POST_request()

		response = home_page(request)

		self.assertEqual(Group.objects.count(), 1)
		new_group = Group.objects.first()
		self.assertEqual(new_group.name, 'New group name')
		self.assertEqual(new_group.alias, 'newgroupalias')
		self.assertEqual(new_group.tags, 'New; group; tags')
		self.assertEqual(new_group.description, 'New group description')

	def test_create_group_correct_name(self):
		#Only restriction: characters => 3 < 27 
		request = create_sample_POST_request()
		
		request.POST['group_name'] = 'Newgroupnamewith28characters'

		response = home_page(request)

		self.assertEqual(Group.objects.count(), 0)

		request.POST['group_name'] = 'da'

		response = home_page(request)

		self.assertEqual(Group.objects.count(), 0)

	def test_create_group_correct_alias(self):
		#Restrictions: No upper case allowed, no symbols, no spaces, <20 characters
		request = create_sample_POST_request()

		request.POST['group_alias'] = 'UPPERCASETEST'
		response = home_page(request)
		self.assertEqual(Group.objects.count(), 0)

		request.POST['group_alias'] = 'space test'
		response = home_page(request)
		self.assertEqual(Group.objects.count(), 0)

		request.POST['group_alias'] = 'alphanumeric/test/'
		response = home_page(request)
		self.assertEqual(Group.objects.count(), 0)

		request.POST['group_alias'] = '12345678910111213test'
		response = home_page(request)
		self.assertEqual(Group.objects.count(), 0)

	def test_create_group_correct_tag(self):
		#Restriction: each tag => 3 < 12, no equal tags
		request = create_sample_POST_request()
		
		request.POST['group_tags'] = 'da; tags; like; a; newbie'

		response = home_page(request)

		self.assertEqual(Group.objects.count(), 0)

		request.POST['group_tags'] = 'dum; dee; dum'

		response = home_page(request)

		self.assertEqual(Group.objects.count(), 0)



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


class SearchTests(TestCase):

	def test_GET_searchs_for_something(self):
		create_sample_database()

		request = HttpRequest()
		request.method = 'GET'
		request.GET['search_group'] = ' '

		response = home_page(request)

		self.assertIn('Teh name', response.content.decode())

	def test_only_displays_GET_on_search(self):
		first_group = Group()
		first_group.name = 'Teh empty tag'
		first_group.alias = 'tehalias'
		first_group.tags = ''
		first_group.description = 'Teh empty description' 
		first_group.save()

		request = HttpRequest()
		request.method = 'GET'
		response = home_page(request)	

		self.assertNotIn('Teh empty tag', response.content.decode())

	def test_search_by_name(self):
		create_sample_database()

		#Testing if find substrings inside Name
		found_groups = search_groups('ame')
		self.assertEqual(len(found_groups), 2)
		self.assertTrue('tehalias' in [a.alias for a in found_groups])
		self.assertTrue('tehalias2' in [a.alias for a in found_groups])


	 	#Testing if find strings inside Name
		found_groups = search_groups('Name')
		self.assertEqual(len(found_groups), 2)
		self.assertTrue('tehalias' in [a.alias for a in found_groups])

	def test_search_by_tag(self):
		create_sample_database()

		# Testing if don't find substrings inside tags
		found_groups = search_groups('tags')
		self.assertEqual(len(found_groups), 1)
		self.assertEqual(found_groups[0].alias, 'tehalias')

		# Testing search 1 tag in multiple groups
		found_groups = search_groups('Teh')
		self.assertEqual(len(found_groups), 2)
		self.assertTrue('tehalias' in [a.alias for a in found_groups])
		self.assertTrue('tehalias2' in [a.alias for a in found_groups])

	def test_search_case_insensitive(self):
		create_sample_database()

		found_groups = search_groups('teh')
		self.assertEqual(len(found_groups), 2)
		self.assertTrue('tehalias' in [a.alias for a in found_groups])
		self.assertTrue('tehalias2' in [a.alias for a in found_groups])

		#Test priority for tags

	def test_search_by_alias(self):
		create_sample_database()

		# Testing if don't find substrings inside alias
		found_groups = search_groups('hal')
		self.assertEqual(len(found_groups), 0)

		# Testing search 1 alias in multiple groups
		found_groups = search_groups('tehalias')
		self.assertEqual(len(found_groups), 1)
		self.assertTrue('tehalias' in [a.alias for a in found_groups])


	#Search by description
	def test_search_by_description(self):
		create_sample_database()

		# Testing if don't find substrings inside descrption
		found_groups = search_groups('crip')
		self.assertEqual(len(found_groups), 0)

		# Testing search 1 alias in multiple groups
		found_groups = search_groups('description')
		self.assertEqual(len(found_groups), 1)
		self.assertTrue('tehalias' in [a.alias for a in found_groups])
