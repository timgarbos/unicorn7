# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from games.models import Game
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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

	return render_to_response('unicorn/games.html', {'games':games})
  
@login_required  
def submit(request):
    return render_to_response('unicorn/submitgames.html', {})
    
    
def showgame(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	return render_to_response('unicorn/showgame.html', {'game':game})