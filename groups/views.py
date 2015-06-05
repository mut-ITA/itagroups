from django.shortcuts import render

from groups.models import Group
# Create your views here.

def home_page(request):
	if request.method == 'POST':
		#Verifications
		if len(request.POST['group_name']) > 27:
			return render(request, 'home.html', {
				'group_success': False,
				'open_popup': True,
				'group_name_error_message': 'O nome do grupo não deve possuir mais de 27 caracteres'
				})
		group = Group()
		group.name = request.POST['group_name']
		group.alias = request.POST['group_alias']
		group.tags = request.POST['group_tags']
		group.description = request.POST['group_description']
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


	 
	#Search search_tags in tags; alias; description