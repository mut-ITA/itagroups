from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from unittest import skip

from groups.views import home_page, view_group, verify_login, signup
from groups.models import Group, User
from groups.HelperMethods.tests import create_sample_database
from groups.HelperMethods.functionalities import search_groups

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


class ViewGroupTests(TestCase):
	
	def test_view_page_returns_correct_html(self):
		create_sample_database()

		request = HttpRequest()

		saved_groups = Group.objects.all()
		response = view_group(request, saved_groups[0].alias)

		self.assertTemplateUsed('view.html')
		self.assertIn(saved_groups[0].name, response.content.decode())

	def test_view_page_returns_to_home_wrong_alias(self):
		response = self.client.get('/groups/this_is_a_wrong_alias/')

		self.assertRedirects(response, '/')
		

class CreateGroupTest(TestCase):

	def sample_group_POST_response(self, name = 'New group name', 
										 alias = 'newgroupalias',
										 tags = 'new; group; tags', 
										 description = 'New group description'):
		response = self.client.post(
			'/', data={	'group_name':  name,
						'group_alias': alias,
						'group_tags': tags,
						'group_description': description
			})

		return response

	def test_create_group_form_redirects_after_POST(self):
		response = self.sample_group_POST_response()

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')

	def test_create_group_POST_save_to_db(self):
		response = self.sample_group_POST_response()

		self.assertEqual(Group.objects.count(), 1)
		new_group = Group.objects.first()
		self.assertEqual(new_group.name, 'New group name')
		self.assertEqual(new_group.alias, 'newgroupalias')
		self.assertEqual(new_group.tags, 'new; group; tags')
		self.assertEqual(new_group.description, 'New group description')


	def test_create_empty_group_validation_error(self):
		response = self.sample_group_POST_response(name = '', alias = '', tags = '', description = '')

		self.assertVerificationError(response, 'Nao pode-se adicionar um grupo vazio!')

	def test_create_empty_group_doesnt_save_db(self):
		response = self.sample_group_POST_response(name = '', alias = '', tags = '', description = '')

		self.assertEqual(Group.objects.count(), 0)


	@skip
	def test_create_group_correct_name(self):
		#Only restriction: characters => 3 < 27 

		response = self.sample_group_POST_response(name = 'Newgroupnamewith28characters')
		self.assertVerificationError(response, 'O nome do grupo deve possuir entre 3 e 27 caracteres')
		self.assertEqual(Group.objects.count(), 0)

		response = self.sample_group_POST_response(name = 'da')
		self.assertVerificationError(response, 'O nome do grupo deve possuir entre 3 e 27 caracteres')
		self.assertEqual(Group.objects.count(), 0)

	@skip
	def test_create_group_correct_alias(self):
		#Restrictions: No upper case allowed, no symbols, no spaces, <20 characters

		response = self.sample_group_POST_response(alias = 'UPPERCASETEST')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 0)

		response = self.sample_group_POST_response(alias = 'space test')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 0)

		response = self.sample_group_POST_response(alias = 'alphanumeric/test/')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 0)

		response = self.sample_group_POST_response(alias = '12345678910111213test')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 0)
		
	@skip
	def test_create_group_correct_tag(self):
		#Restriction: each tag => 3 < 12, no equal tags
		
		response = self.sample_group_POST_response(tags = 'da; tags; like; a; newbie')
		self.assertVerificationError(response, 'Todas as tags devem possuir entre 3 e 12 caracteres')
		self.assertEqual(Group.objects.count(), 0)

		response = self.sample_group_POST_response(tags = 'dum; dee; dum')
		self.assertVerificationError(response, 'Não podem haver tags iguais')
		self.assertEqual(Group.objects.count(), 0)

	def assertVerificationError(self, response, expected_error):
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		self.assertContains(response, expected_error)


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

class UserAccountTest(TestCase):

	def test_login_url_resolves_to_login_page(self):
		found = resolve('/login')
		self.assertEqual(found.func, verify_login)

	def test_POST_new_user_redirects_signup(self):
		response = self.client.post('/login', data = {'username_input': 'newUser'})

		self.assertEqual(response.status_code, 302)

		self.assertRedirects(response, '/signup/')

	def test_POST_save_user_to_db(self):
		self.client.cookies['LOGSESSID'] = 'User1'

		response = self.client.post('/signup/', data = {'apelido_input': 'newApelido', 'turma_input': 'newTurma'})

		self.assertEqual(User.objects.count(), 1)
		new_user = User.objects.first()

		self.assertEqual(new_user.access_token, 'User1')

	def test_POST_user_redirects_home(self):
		User.objects.create(access_token = 'oldUser')

		response = self.client.post('/login', data = {'username_input': 'oldUser'})

		self.assertEqual(response.status_code, 302)

		self.assertRedirects(response, '/')

	def test_signup_page_returns_correct_html(self):
		request = HttpRequest()
		response = signup(request)
		expected_html = render_to_string('signup.html')
		self.assertEqual(response.content.decode(), expected_html)

	# def test_user_greeting_message_home_page(self):
	# 	self.client.cookies['LOGSESSID'] = 'User1'

	# 	response = self.client.get('/')

	# 	self.fail(response.content.decode())
	# 	self.assertContains(response, 'Bem vindo, User1')

	# def test_login_creates_cookie(self):
		
	# 	response = self.client.post('/login', data = {'username_input': 'newUser'})

	# 	cookies = response.client.cookies.items()

	# 	self.assertEqual(len(cookies), 2)

	# 	self.assertTrue('LOGSESSID' in [cks.key for cks in cookies] )
