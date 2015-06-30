from django.shortcuts import render

from groups.models import Group, User

def verification(request, name, alias, tags, description):
		passed = True
		group_name_error_message = ''
		group_alias_error_message = ''
		group_tags_error_message = ''
		group_description_error_message = ''

		#Name verification
		if len(name.strip()) > 27 or len(name.strip()) < 3:

			passed = False
			group_name_error_message = 'O nome do grupo deve possuir entre 3 e 27 caracteres'

		#Alias verification
		if len(alias.strip()) > 20 or ' ' in alias or (not alias.islower()) or (not alias.isalnum()):
			passed = False
			group_alias_error_message = 'Minusculo, sem simbolos, sem espaço'

		#Alias originality
		for g in Group.objects.all():
			if alias is g.alias:
				passed = False
				group_alias_error_message = 'Já existe um grupo com esse alias'
			if name is g.name:
				passed = False
				group_name_error_message = 'Já existe um grupo com esse nome'

		#Tag verification
		for tag in tags.strip().split(';'):
			for n in range(tags.split(';').index(tag) + 1, len(tags.split(';'))):
				if tag.strip() == tags.split(';')[n].strip():
					passed = False
					group_tags_error_message = 'Não podem haver tags iguais'

			if len(tag.strip()) > 12 or len(tag.strip()) < 3:
				passed = False
				group_tags_error_message = 'Todas as tags devem possuir entre 3 e 12 caracteres'



		if passed:
			return None

		return render(request, 'home.html', {
					'group_success': False,
					'open_popup': True,
					'group_name_error_message': group_name_error_message,
					'group_alias_error_message': group_alias_error_message,
					'group_tags_error_message': group_tags_error_message,
					'group_description_error_message': group_description_error_message,
					'group_name_value': name,
					'group_alias_value': alias,
					'group_tags_value': tags,
					'group_description_value': description
					})

def search_groups(search_tags):	
	all_groups = Group.objects.all()
	#Add priority
	#for g in all_groups:
	#	g.priority = 0
	#Search search_tags inside group_name
	found_groups = []
	for g in all_groups:
		for tag in search_tags.split(' '):
			# Search in name (can be substring)
			if g.name.strip().lower().find(tag.lower()) != -1:
				found_groups.append(g)
				break
			# Search in tags
			if tag.lower() in [t.strip().lower() for t in g.tags.split(';')]:
				found_groups.append(g)
				break
			# Search in alias
			if tag.lower() == g.alias:
				found_groups.append(g)
				break
			# Search in description
			if tag.lower() in [d.strip().lower() for d in g.description.split(' ')]:
				found_groups.append(g)
				break

	return found_groups
