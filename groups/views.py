from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.contrib.auth.views import logout

from groups.models import Group, User
from groups.forms import GroupForm
from groups.HelperMethods.functionalities import verification, search_groups



def home_page(request):

	# Home page get is searching for groups
	if request.method == 'POST':
		name = request.POST['name']
		alias = request.POST['alias']
		tags = request.POST['tags']
		description = request.POST['description']

		group = Group(	name = name,
						alias = alias,
						tags = tags,
						description = description)

		try:
			group.full_clean()
			group.save()
		except ValidationError:
			error = "Nao pode-se adicionar um grupo vazio!"
			return render(request, 'home.html', {'group_description_error_message': error})

		if verification(request, name, alias, tags, description):
		 	return verification(request, name, alias, tags, description)




		#return render(request, 'home.html', {
		# 	'group_success': True,
		# 	'open_popup': True,
		# 	'group_name': group.name,
		# 	'group_tags': group.tags,
		# 	'group_alias': group.alias,
		# 	'group_description': group.description
		# 	})
		return redirect('home')

	if request.method == 'GET':
		search_tags = request.GET.get('search_group', '')
		if search_tags != '':
			found_groups = search_groups(search_tags)
			return render(request, 'home.html', {
				'groups': found_groups
				})

	return render(request, 'home.html', {'form': GroupForm()})


def view_group(request, group_alias):
	found_groups = search_groups(group_alias)
	if found_groups:
		if request.method == 'POST':
			username = request.COOKIES['LOGSESSID']
			if User.objects.filter(access_token = username):
				User.objects.filter(access_token = username)[0].groups.add(found_groups[0])
		return render(request, 'view_group.html', {
			'group_name': found_groups[0].name,
			'users': found_groups[0].user_set.all()
			})
	return redirect('home')


def verify_login(request):

	user = request.POST['username_input']

	response = redirect('home') if User.objects.filter(access_token = user) else redirect('sign_up')

	#Cookie username

	response.set_cookie('LOGSESSID', user)

	return response


def logout(self):
	response = redirect ('home')
	response.delete_cookie('LOGSESSID')

	return response


def signup(request):

	if request.method == 'POST':

		# Writing less
		apelido = request.POST['apelido_input']
		turma = request.POST['turma_input']

		#Getting the cookie
		username = request.COOKIES['LOGSESSID']

		response = redirect('home')

		if User.objects.filter(access_token = username):
			response.set_cookie('LOGSESSID', username)

			return response

		user = User()
		user.access_token = username
		user.apelido = apelido
		user.turma = turma
		user.save()

		return response

	return render(request, 'signup.html')
