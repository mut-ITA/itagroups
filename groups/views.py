from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.contrib.auth.views import logout

from groups.models import Group, User

from groups.HelperMethods.functionalities import verification, search_groups, create_session



def home_page(request):

	# Home page get is searching for groups
	if request.method == 'POST':
		name = request.POST['group_name']
		alias = request.POST['group_alias']
		tags = request.POST['group_tags']
		description = request.POST['group_description']

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

	return render(request, 'home.html')

	
def view_group(request, group_alias):
	found_groups = search_groups(group_alias)
	if found_groups:
		group = found_groups[0]
		if request.method == 'POST':
			id_ = request.session['id']
			user = User.objects.filter(id = id_)
			if user:
				user[0].groups.add(group)
		return render(request, 'view_group.html', {
			'group': group,
			'users': group.user_set.all(),
			'user_ids': [u.id for u in group.user_set.all()]
			})
	return redirect('home')


def verify_login(request):
	if request.method == 'POST':
		access_token = request.POST['username_input']

		user = User.objects.filter(access_token = access_token)

		if user:
			#Session username
			response = redirect('home')
			create_session(request, user[0].id, user[0].apelido, access_token)

		else:
			response = redirect('sign_up')
			request.session['access_token'] = access_token
		
		return response	

	return redirect('home')


def logout(request):
	response = redirect ('home')
	request.session.flush()

	return response


def signup(request):
	
	if request.method == 'POST':

		# Writing less
		apelido = request.POST['apelido_input']
		turma = request.POST['turma_input']

		#Getting the cookie
		access_token = request.session['access_token']

		response = redirect('home')
		#Nao precisa mais dessa verificação pois estamos usando session.
		user = User.objects.filter(access_token = access_token)

		if user:
			create_session(request, user[0].id, user[0].apelido, access_token)
			return response

		user = User()
		user.access_token = access_token
		user.apelido = apelido
		user.turma = turma
		user.save()

		user = User.objects.filter(access_token = access_token)

		create_session(request, user[0].id, user[0].apelido, access_token)

		return response

	return render(request, 'signup.html')

def view_user(request, id_):
	if User.objects.filter(id = id_):
		return render(request, 'view_user.html', {
			'apelido': User.objects.filter(id = id_)[0].apelido,
			'groups': User.objects.filter(id = id_)[0].groups.all()
			})
	return redirect('home')

def self_user(request):
	id_ = request.session['id']
	if User.objects.filter(id = id_):

		return redirect ('/users/' + str(id_) + '/')
	return redirect('home')
