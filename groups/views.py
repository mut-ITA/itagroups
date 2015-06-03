from django.shortcuts import render

from groups.models import Group
# Create your views here.

def home_page(request):
	if request.method == 'POST':
		#Verificacoes
		group = Group()
		group.name = request.POST['group_name']
		group.alias = request.POST['group_alias']
		group.tags = request.POST['group_tags']
		group.description = request.POST['group_description']
		group.save()

		return render(request, 'home.html', {
			'group_success': True, 
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
	all_groups = Group.objects.all()\
	#Add priority
	#for g in all_groups:
	#	g.priority = 0
	#Search search_tags inside group_name
	found_groups = []
	for g in all_groups:
		for tag in search_tags.split(' '):
			if tag.lower() in [t.strip().lower() for t in g.tags.split(';')]:
				found_groups.append(g)
				continue

	return found_groups


	 
	#Search search_tags in tags; alias; description