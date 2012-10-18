# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from games.models import Game, GameForm,GamePlatform,GameCategory,GamePlatformLink,ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import modelformset_factory


def listgames(request):
	game_list = Game.objects.all()
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
  
@login_required  
def submit(request):
    return render_to_response('unicorn/submitgames.html', {'topnav':'submit'})
    
    
def showgame(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	return render_to_response('unicorn/showgame.html', {'topnav':'showgame','game':game})


def editgamebasic(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	formset = GameForm(instance=game)
	return render_to_response('unicorn/editgame_basic.html', {'topnav':'editgamebasic','game':game,'form':formset})

def editgamecontact(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	formset = ContactForm(instance=game)
	return render_to_response('unicorn/editgame_contact.html', {'topnav':'editgamecontact','game':game,'form':formset})

def editgameplatforms(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	links = []
	for platform in GamePlatform.objects.all():
		link = GamePlatformLink(platform=platform,game=game)
		for l in GamePlatformLink.objects.filter(game=game):
			if(l.platform == platform):
				link = l
				hasLink = True
		links.append({'platform':link.platform,'url':link.url})

	return render_to_response('unicorn/editgame_links.html', {'topnav':'editgameplatforms','game':game,'links':links})

def editgamecategories(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	cats = []
	for category in GameCategory.objects.all():
		has = False
		for c in game.categories.all():
			if(c.id == category.id):
				has = True
		cats.append({'category':category,'has':has})

	return render_to_response('unicorn/editgame_categories.html', {'topnav':'editgamemedia','game':game,'categories':cats})

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

