from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from unittest import skip

from groups.views import home_page, view_group, verify_login, signup, logout, view_user, self_user
from groups.models import Group, User
from groups.HelperMethods.tests import create_sample_database, create_sample_user_database
from groups.HelperMethods.functionalities import search_groups
from groups.forms import GroupForm, ERRORS
from groups.HelperMethods.functionalities import search_groups, create_session

# Create your tests here.

class ItemFormTest(TestCase):

	def test_form_item_input_has_placeholder_and_css_classes(self):
		form = GroupForm()
		self.assertIn('placeholder="Entre o nome do grupo"', form.as_p())
		self.assertIn('class="form-control input-medium"', form.as_p())

	def test_form_validation_for_blank_items(self):
		form = GroupForm(data={'name': '', 'alias': '', 'tags': '', 'description': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['name'],
			[ERRORS.EMPTY_NAME]
		)
		self.assertEqual(
			form.errors['alias'],
			[ERRORS.EMPTY_ALIAS]
		)
		self.assertEqual(
			form.errors['tags'],
			[ERRORS	.EMPTY_TAGS]
		)


class HomePageTest(TestCase):

	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_home_page_uses_group_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], GroupForm)

class ViewGroupTests(TestCase):

	def sample_group_view_POST_response(self, alias):
		response = self.client.post(
			'/groups/'+ alias + '/', data={'access_token': 'Username1'
			})

		return response

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

class JoinGroupTest(TestCase):

	def sample_group_view_POST_response(self, alias, id_):
		session = self.client.session
		session['id'] = id_
		session.save()
		response = self.client.post(
			'/groups/'+ alias + '/', data={'access_token': 'Username1'
			})

		return response

	def test_POST_user_join_group_db(self):
		create_sample_database()
		create_sample_user_database()

		saved_groups = Group.objects.all()

		response = self.sample_group_view_POST_response(saved_groups[0].alias, Group.objects.all()[0].id)

		self.assertEqual(saved_groups[0].user_set.all().count(), 1)

		self.assertEqual(saved_groups[0].user_set.all()[0].access_token, "Username1")


class CreateGroupTest(TestCase):

	def sample_group_POST_response(self, name = 'New group name',
										 alias = 'newgroupalias',
										 tags = 'new; group; tags',
										 description = 'New group description'):
		session = self.client.session
		session['id'] = '2'
		session['apelido'] = 'TestApelido'
		session['access_token'] = 'TestUser'
		session.save()
		response = self.client.post(
			'/', data={	'group_name':  name,
						'group_alias': alias,
						'group_tags': tags,
						'group_description': description
			})

		return response

	def test_redirects_login_page_if_without_login(self):
		pass

	# def test_create_group_form_redirects_after_POST(self):
	# 	response = self.sample_group_POST_response()

	# 	self.assertEqual(response.status_code, 302)
	# 	self.assertRedirects(response, '/')

	def test_create_group_POST_save_to_db(self):
		response = self.sample_group_POST_response()

		self.assertEqual(Group.objects.count(), 1)
		new_group = Group.objects.first()
		self.assertEqual(new_group.name, 'New group name')
		self.assertEqual(new_group.alias, 'newgroupalias')
		self.assertEqual(new_group.tags, 'new; group; tags')
		self.assertEqual(new_group.description, 'New group description')


	# @skip
	# def test_create_empty_group_validation_error(self):
	#  	response = self.sample_group_POST_response(name = '', alias = '', tags = '', description = '')
	# 	self.assertIn(ERRORS.EMPTY_NAME, response.content.decode())
	#  	self.assertVerificationError(response, 'Nao pode-se adicionar um grupo vazio!')


	def test_create_empty_group_doesnt_save_db(self):
		response = self.sample_group_POST_response(name = '', alias = '', tags = '', description = '')

		self.assertEqual(Group.objects.count(), 0)

	def test_create_group_correct_name(self):
		#Only restriction: characters => 3 < 27

		response = self.sample_group_POST_response(name = 'Newgroupnamewith28characters')
		self.assertVerificationError(response, 'O nome do grupo deve possuir entre 3 e 27 caracteres')
		self.assertEqual(Group.objects.count(), 0)

		response = self.sample_group_POST_response(name = 'da')
		self.assertVerificationError(response, 'O nome do grupo deve possuir entre 3 e 27 caracteres')
		self.assertEqual(Group.objects.count(), 0)


	def test_create_group_correct_alias(self):
		#Restrictions: No upper case allowed, no symbols, no spaces, <20 characters
		create_sample_database()

		response = self.sample_group_POST_response(alias = 'tehalias')
		self.assertEqual(Group.objects.count(), 2)

		response = self.sample_group_POST_response(alias = 'UPPERCASETEST')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 2)

		response = self.sample_group_POST_response(alias = 'space test')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 2)

		response = self.sample_group_POST_response(alias = 'alphanumeric/test/')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 2)

		response = self.sample_group_POST_response(alias = '12345678910111213test')
		self.assertVerificationError(response, 'Minusculo, sem simbolos, sem espaço')
		self.assertEqual(Group.objects.count(), 2)


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

	def test_logout_url_resolves_to_login_page(self):
		found = resolve('/logout')
		self.assertEqual(found.func, logout)

	def test_GET_in_login_redirects_home(self):
		response = self.client.get('/login')

		self.assertEqual(response.status_code, 302)

		self.assertRedirects(response, '/')

	def test_POST_new_user_redirects_signup(self):
		response = self.client.post('/login', data = {'username_input': 'newUser'})

		self.assertEqual(response.status_code, 302)

		self.assertRedirects(response, '/signup/')

	def test_POST_signup_save_user_to_db(self):
		session = self.client.session
		session['access_token'] = 'User1'
		session.save()

		response = self.client.post('/signup/', data = {'apelido_input': 'newApelido', 'turma_input': 'newTurma'})

		self.assertEqual(User.objects.count(), 1)
		new_user = User.objects.first()

		self.assertEqual(new_user.access_token, 'User1')

	def test_POST_user_redirects_home(self):
		User.objects.create(access_token = 'oldUser')

		response = self.client.post('/login', data = {'username_input': 'oldUser'})

		session = self.client.session

		self.assertEqual(session['access_token'], 'oldUser')

		self.assertEqual(response.status_code, 302)

		self.assertRedirects(response, '/')

	def test_signup_page_returns_correct_html(self):
		request = HttpRequest()
		response = signup(request)
		expected_html = render_to_string('signup.html')
		self.assertEqual(response.content.decode(), expected_html)


	def test_logout_redirects_to_home(self):
		response = self.client.get('/logout')

		self.assertEqual(response.status_code, 302)

		self.assertRedirects(response, '/')

class ViewUserTest(TestCase):
	def test_view_user_page_returns_correct_html(self):
		create_sample_user_database()

		saved_users = User.objects.all()
		response = self.client.get('/users/%s/' %saved_users[0].id)

		self.assertTemplateUsed('view_user.html')
		self.assertIn(saved_users[0].apelido, response.content.decode())

	def test_view_page_returns_to_home_wrong_alias(self):
		response = self.client.get('/users/02020200222/')

		self.assertRedirects(response, '/')

	def test_view_user_self_page_redirect_correct_page(self):
		create_sample_user_database()
		user = User.objects.all()

		session = self.client.session
		session['id']	= user[0].id
		session['apelido'] = user[0].apelido
		session['access_token'] = user[0].access_token
		session.save()

		response = self.client.get('/users/me')

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/users/'+ str(user[0].id) +'/')

	def test_view_user_self_page_wrong_id_redirect_home_page(self):
		create_sample_user_database()
		user = User.objects.all()

		session = self.client.session
		session['id']	= 1321321
		session['apelido'] = user[0].apelido
		session['access_token'] = user[0].access_token
		session.save()

		response = self.client.get('/users/me')

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')





class UserExitGroupTest(TestCase):
	def test_leave_group_redirects_to_group_page(self):
		create_sample_database()
		create_sample_user_database()
		saved_groups = Group.objects.all()
		saved_users = User.objects.all()
		sample_user = saved_users[0]
		sample_group = saved_groups[0]
		sample_user.groups.add(sample_group)

		session = self.client.session
		session['id']	= sample_user.id
		session['apelido'] = sample_user.apelido
		session['access_token'] = sample_user.access_token
		session.save()

		response = self.client.post('/groups/'+ sample_group.alias + '/leave')
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/groups/' + sample_group.alias + '/')

	def test_leave_group_removes_user_from_group_on_db(self):
		create_sample_database()
		create_sample_user_database()
		saved_groups = Group.objects.all()
		saved_users = User.objects.all()
		sample_user = saved_users[0]
		sample_group = saved_groups[0]
		sample_user.groups.add(sample_group)

		self.assertEqual(len(sample_user.groups.all()), 1)

		session = self.client.session
		session['id']	= sample_user.id
		session['apelido'] = sample_user.apelido
		session['access_token'] = sample_user.access_token
		session.save()

		response = self.client.post('/groups/' + sample_group.alias + '/leave')

		self.assertEqual(len(sample_user.groups.all()), 0)

	def test_leave_group_from_user_redirects_to_user_page(self):
		create_sample_database()
		create_sample_user_database()
		saved_groups = Group.objects.all()
		saved_users = User.objects.all()
		sample_user = saved_users[0]
		sample_group = saved_groups[0]
		sample_user.groups.add(sample_group)

		session = self.client.session
		session['id']	= sample_user.id
		session['apelido'] = sample_user.apelido
		session['access_token'] = sample_user.access_token
		session.save()

		response = self.client.get('/groups/'+ sample_group.alias + '/leave')
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/users/' + str(sample_user.id) + '/')

	def test_leave_group_without_session_from_user_redirects_to_home(self):
		create_sample_database()
		create_sample_user_database()
		saved_groups = Group.objects.all()
		saved_users = User.objects.all()
		sample_user = saved_users[0]
		sample_group = saved_groups[0]
		sample_user.groups.add(sample_group)

		response = self.client.get('/groups/'+ sample_group.alias + '/leave')
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')

	def test_leave_group_without_session_from_groups_redirects_to_home(self):
		create_sample_database()
		create_sample_user_database()
		saved_groups = Group.objects.all()
		saved_users = User.objects.all()
		sample_user = saved_users[0]
		sample_group = saved_groups[0]
		sample_user.groups.add(sample_group)

		response = self.client.post('/groups/'+ sample_group.alias + '/leave')
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')

	@skip
	def test_user_greeting_message_home_page(self):
	 	pass
