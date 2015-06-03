from django.shortcuts import render

# Create your views here.

def home_page(request):
	if request.method == 'POST':
		#Verificacoes
		group_name = request.POST['group_name']
		group_alias = request.POST['group_alias']
		group_tags = request.POST['group_tags']
		group_description = request.POST['group_description']
		return render(request, 'home.html', {
			'group_success': True, 
			'group_name': group_name,
			'group_tags': group_tags,
			'group_alias': group_alias,
			'group_description': group_description 
			})

	return render(request, 'home.html')
