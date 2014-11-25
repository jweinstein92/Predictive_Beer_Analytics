from app.models import Comment
from app.models import Location
from app.models import AvbsRange
from app.models import BeerType
from app.models import Abvs
from app.models import Word
from app.models import Color
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from app.forms import CommentForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden


from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot


def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def description(request):

    topList = Comment.objects.all()[:5]
    bottomList = Comment.objects.all().order_by('-id')[:5]

    return render_to_response('description.html',{'topList' : topList, 'bottomList' : bottomList }, context_instance=RequestContext(request))

def listEntries(request):

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            newComment = Comment()
            newComment.text = request.POST.get('text', '')
            newComment.save()

    form = CommentForm()
    commentList = Comment.objects.all()




    return render_to_response('list.html',{'commentList' : commentList, 'form' : form }, context_instance=RequestContext(request))



def map(request):

    return render_to_response('map.html',{}, context_instance=RequestContext(request))

def prediction(request):

    locations = Location.objects.all()
    avbsRanges = AvbsRange.objects.all()
    beerTypes = BeerType.objects.all()

    return render_to_response('prediction.html',{'locationList': locations , 'avbsRangesList': avbsRanges , 'beerTypeList' : beerTypes}, context_instance=RequestContext(request))

def getPrediction(request):


    return render_to_response('Histogram.html',{'title' : "Title" , 'description' : "Description thi is the juicy part!!!"}, context_instance=RequestContext(request))

