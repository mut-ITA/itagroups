from django.shortcuts import render

from groups.models import Group
# Create your views here.

def home_page(request):
	if request.method == 'POST':

		#Writing less
		name = request.POST['group_name']
		alias = request.POST['group_alias']
		tags = request.POST['group_tags']
		description = request.POST['group_description']

		#Verifications

		verification = True
		group_name_error_message = ''
		group_alias_error_message = ''
		group_tags_error_message = ''
		group_description_error_message = ''

		#Name verification
		if len(name) > 27:

			verification = False
			group_name_error_message = 'O nome do grupo não deve possuir mais de 27 caracteres'

		#Alias verification
		if len(alias) > 20 or ' ' in alias or (not alias.islower()) or (not alias.isalpha()):

			verification = False
			group_alias_error_message = 'Minusculo, sem simbolos, sem espaço'

		
		if not verification :
			
			return render(request, 'home.html', {
					'group_success': False,
					'open_popup': True,
					'group_name_error_message': group_name_error_message,
					'group_alias_error_message': group_alias_error_message,
					'group_tags_error_message': group_tags_error_message,
					'group_description_error_message': group_description_error_message
					})

		group = Group()
		group.name = name
		group.alias = alias
		group.tags = tags
		group.description = description
		group.save()

		return render(request, 'home.html', {
			'group_success': True,
			'open_popup': True, 
			'group_name': group.name,
			'group_tags': group.tags,
			'group_alias': group.alias,
			'group_description': group.description
			})
	if request.method == 'GET':
		search_tags = request.GET.get('search_group', '')
		if search_tags != '':
			found_groups = search_groups(search_tags)
			return render(request, 'home.html', {
				'groups': found_groups
				})

	return render(request, 'home.html')



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
