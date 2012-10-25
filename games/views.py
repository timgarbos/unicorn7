# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from games.models import Game, GameForm,GamePlatform,GameCategory,GamePlatformLink,ContactForm,GameSubmitForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from djangoratings.views import AddRatingFromModel


def listgames(request):
	game_list = Game.objects.all().filter(status=Game.LIVE_STATUS)
	paginator = Paginator(game_list, 20)
	page = request.GET.get('page')
	try:
		games = paginator.page(page)
 	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		games = paginator.page(1)
 	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		games = paginator.page(paginator.num_pages)
	categories = GameCategory.objects.all()
	platforms = GamePlatform.objects.all()
	return render_to_response('unicorn/games.html', {'topnav':'listgames','games':games,'categories':categories,'platforms':platforms})
  
#@login_required  
@csrf_protect
def submitgamebasic(request):
	context = {'topnav':'submitgamebasic'}
	if request.method == 'POST': 
		game = Game()
		form = GameSubmitForm(request.POST,instance = game) 
		if form.is_valid():
			form.save()
			context['success'] = True
			return HttpResponseRedirect(reverse('games.views.submitgameplatforms', kwargs={'id': game.id}))
		else:
			context['error'] = True 
	else:
		form = GameSubmitForm()

	context['form'] = form;
	return render_to_response('unicorn/submitgame_basic.html',context,context_instance=RequestContext(request))

#@login_required  
@csrf_protect
def submitgameplatforms(request,id="-1"):
	context = {'topnav':'submitgameplatforms'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')


	if request.method == 'POST': 
		game.platforms.clear()
		for platform in GamePlatform.objects.all():
			if (str(platform.id) in request.POST):
				url = request.POST[str(platform.id)]
				if url:
					link = GamePlatformLink(platform=platform,game=game,url=url)
					link.save()
		game.save()
		context['success'] = True 
		return HttpResponseRedirect(reverse('games.views.submitgamecategories', kwargs={'id': game.id}))
	
	links = []
	for platform in GamePlatform.objects.all():
		link = GamePlatformLink(platform=platform,game=game)
		for l in GamePlatformLink.objects.filter(game=game):
			if(l.platform == platform):
				link = l
				hasLink = True
		links.append({'platform':link.platform,'url':link.url})

	context['game'] = game;
	context['links'] = links;
	return render_to_response('unicorn/submitgame_links.html', context,context_instance=RequestContext(request))

#@login_required  
@csrf_protect
def submitgamecategories(request,id="-1"):
	context = {'topnav':'submitgamecategories'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	
	if request.method == 'POST': 
		game.categories.clear()
		for category in GameCategory.objects.all():
			if (str(category.id) in request.POST):
				game.categories.add(category)
		game.save()
		context['success'] = True 
		return HttpResponseRedirect(reverse('games.views.submitgamecontact', kwargs={'id': game.id}))
	cats = []
	for category in GameCategory.objects.all():
		has = False
		for c in game.categories.all():
			if(c.id == category.id):
				has = True
		cats.append({'category':category,'has':has})

	context['game'] = game;
	context['categories'] = cats;
	return render_to_response('unicorn/submitgame_categories.html', context,context_instance=RequestContext(request))

#@login_required  
@csrf_protect
def submitgamecontact(request,id="-1"):
	context = {'topnav':'submitgamecontact'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)


	if request.method == 'POST': 
		form = ContactForm(request.POST,instance = game) 
		if form.is_valid():
			form.save()
			context['success'] = True 
			return HttpResponseRedirect(reverse('games.views.submitgamepublish', kwargs={'id': game.id}))
		else:
			context['error'] = True 
	else:
		form = ContactForm(instance=game)
	context['form'] = form;
	context['game'] = game;
	return render_to_response('unicorn/submitgame_contact.html', context,context_instance=RequestContext(request))

@csrf_protect
def submitgamepublish(request,id="-1"):
	context = {'topnav':'submitgamepublish'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)


	if request.method == 'POST': 
			context['success'] = True 
			game.status = Game.LIVE_STATUS
			game.save()
			return HttpResponseRedirect(reverse('games.views.submitgamepublished', kwargs={'id': game.id}))
	context['game'] = game;
	return render_to_response('unicorn/submitgame_publish.html', context,context_instance=RequestContext(request))

def submitgamemedia(request,id="-1"):
	return render_to_response('unicorn/submitgame_categories.html', )

def submitgamepublished(request,id="-1"):
	context = {'topnav':'submitgamepublished'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)

	context['game'] = game;
	return render_to_response('unicorn/submitgame_published.html', context,context_instance=RequestContext(request))

    
def showgame(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	showEdit = True
	platforms = GamePlatformLink.objects.filter(game=game)
	return render_to_response('unicorn/showgame.html', {'topnav':'showgame','game':game,'platforms':platforms,'showEditOptions':showEdit},context_instance=RequestContext(request))



@csrf_protect
def editgamebasic(request,id="-1"):
	context = {'topnav':'editgamebasic'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	if request.method == 'POST': 
		form = GameForm(request.POST,instance = game) 
		if form.is_valid():
			form.save()
			context['success'] = True 
		else:
			context['error'] = True 
	else:
		form = GameForm(instance=game)

	context['form'] = form;
	context['game'] = game;
	return render_to_response('unicorn/editgame_basic.html', context,context_instance=RequestContext(request))

@csrf_protect
def editgamecontact(request,id="-1"):
	context = {'topnav':'editgamecontact'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)


	if request.method == 'POST': 
		form = ContactForm(request.POST,instance = game) 
		if form.is_valid():
			form.save()
			context['success'] = True 
		else:
			context['error'] = True 
	else:
		form = ContactForm(instance=game)
	context['form'] = form;
	context['game'] = game;
	return render_to_response('unicorn/editgame_contact.html', context,context_instance=RequestContext(request))

@csrf_protect
def editgameplatforms(request,id="-1"):
	context = {'topnav':'editgameplatforms'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')


	if request.method == 'POST': 
		game.platforms.clear()
		for platform in GamePlatform.objects.all():
			if (str(platform.id) in request.POST):
				url = request.POST[str(platform.id)]
				if url:
					link = GamePlatformLink(platform=platform,game=game,url=url)
					link.save()
		game.save()
		context['success'] = True 
	
	links = []
	for platform in GamePlatform.objects.all():
		link = GamePlatformLink(platform=platform,game=game)
		for l in GamePlatformLink.objects.filter(game=game):
			if(l.platform == platform):
				link = l
				hasLink = True
		links.append({'platform':link.platform,'url':link.url})

	context['game'] = game;
	context['links'] = links;
	return render_to_response('unicorn/editgame_links.html', context,context_instance=RequestContext(request))

@csrf_protect
def editgamecategories(request,id="-1"):
	context = {'topnav':'editgamecategories'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	
	if request.method == 'POST': 
		game.categories.clear()
		for category in GameCategory.objects.all():
			if (str(category.id) in request.POST):
				game.categories.add(category)
		game.save()
		context['success'] = True 
	
	cats = []
	for category in GameCategory.objects.all():
		has = False
		for c in game.categories.all():
			if(c.id == category.id):
				has = True
		cats.append({'category':category,'has':has})

	context['game'] = game;
	context['categories'] = cats;
	return render_to_response('unicorn/editgame_categories.html', context,context_instance=RequestContext(request))

def editgamemedia(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	cats = []
	for category in GameCategory.objects.all():
		has = False
		for c in game.categories:
			if(c.id == category.id):
				has = True
		cats.append({'category':category,'has':has})

	return render_to_response('unicorn/editgame_categories.html', {'topnav':'editgamemedia','game':game,'categories':cats})

def rategame(request,id="-1",type="-1"):


	if request.method == 'GET': 
		rate = request.GET['rate']
		field = ''
		if type=='0':
			field = 'rating_fun'
		if type=='1':
			field = 'rating_novelty'
		if type=='2':
			field = 'rating_humour'
		if type=='3':
			field = 'rating_visuals'
		if type=='4':
			field = 'rating_audio'

		params = {
		    'model': 'game',
		    'object_id': id,
		    'app_label': 'games',
		    'field_name': field, # this should match the field name defined in your model
		    'score': rate, # the score value they're sending
		}
		response = AddRatingFromModel()(request, **params)
		
		return HttpResponse(content=response.content)
	return HttpResponse(content='')