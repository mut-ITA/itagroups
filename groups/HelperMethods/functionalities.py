from django.shortcuts import render

from groups.models import Group

def verification(request, name, alias):
		passed = True
		group_name_error_message = ''
		group_alias_error_message = ''
		group_tags_error_message = ''
		group_description_error_message = ''

		#Name verification
		if len(name) > 27:

			passed = False
			group_name_error_message = 'O nome do grupo não deve possuir mais de 27 caracteres'

		#Alias verification
		if len(alias) > 20 or ' ' in alias or (not alias.islower()) or (not alias.isalpha()):

			passed = False
			group_alias_error_message = 'Minusculo, sem simbolos, sem espaço'

		if passed:
			return None

		return render(request, 'home.html', {
					'group_success': False,
					'open_popup': True,
					'group_name_error_message': group_name_error_message,
					'group_alias_error_message': group_alias_error_message,
					'group_tags_error_message': group_tags_error_message,
					'group_description_error_message': group_description_error_message
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