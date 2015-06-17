from groups.models import Group
from django.http import HttpRequest

def create_sample_database():
	first_group = Group()
	first_group.name = 'Teh name'
	first_group.alias = 'tehalias'
	first_group.tags = 'Teh; tags'
	first_group.description = 'Teh description' 
	first_group.save()

	second_group = Group()
	second_group.name = 'Teh name2'
	second_group.alias = 'tehalias2'
	second_group.tags = 'Teh; tags2'
	second_group.description = 'Teh description2'
	second_group.save()	

def create_sample_POST_request():
	request = HttpRequest()
	request.method = 'POST'
	request.POST['group_name'] = 'New group name'
	request.POST['group_alias'] = 'newgroupalias'
	request.POST['group_tags'] = 'New; group; tags'
	request.POST['group_description'] = 'New group description'

	return request