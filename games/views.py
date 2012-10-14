# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from games.models import Game


def listgames(request):
    return render_to_response('unicorn/games.html', {})
  
@login_required  
def submit(request):
    return render_to_response('unicorn/submitgames.html', {})
    
    
def showgame(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	return render_to_response('unicorn/showgame.html', {'game':game})