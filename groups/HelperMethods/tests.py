from groups.models import Group, User
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

def create_sample_user_database():
	first_user = User()
	first_user.access_token = 'Username1'
	first_user.apelido = 'Apelido1'
	first_user.turma = 'T17'
	first_user.save() 

	second_user = User()
	second_user.access_token = 'Username2'
	second_user.apelido = 'Apelido2'
	second_user.turma = 'T20'
	second_user.save() 