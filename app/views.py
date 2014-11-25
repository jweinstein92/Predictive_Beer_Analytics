import sys
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
import jsonpickle as jpickle
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden


from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot


def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def description(request):

    topList = Word.objects.all()[:5]
    bottomList = Word.objects.all().order_by('rating')[:5]
    resultList = []
    if request.method == 'POST' and request.POST.get('qry') != "":
        query = request.POST.get('qry')

        resultList = Word.objects.filter(Q(value__icontains=query)).order_by('-rating')[:5]


    return render_to_response('description.html',{'topList' : topList, 'bottomList' : bottomList, 'resultList' : resultList }, context_instance=RequestContext(request))

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

    if request.method == 'POST':
        location = request.POST.get('location')
        beerType = request.POST.get('beerType')
        avbs = request.POST.get('avbs')
        description = request.POST.get('description')
        color = request.POST.get('color')



        #try:
        #    keywordsFile = open('C:/keywords.json', 'rb')
       # except:
        #    print 'Keywords.json not found.'
        #    sys.exit()

       # try:
        #    f = keywordsFile.read()
        ##    keywordsDict = jpickle.decode(f)
       # except:
          #  keywordsDict = []
       #     print 'Keywords list corrupted'
       #     sys.exit()
       # keywordsFile.close()

        # Sorted by average rating
       # SortedByRating = {}
      #  SortedByRating['keywords'] = []
      #  SortedByRating['ratings'] = []
       # SortedByRating['usage'] = []
       # for word in sorted(keywordsDict.items(), key=lambda k: (k[1][0] / k[1][1]), reverse=True):
        #    ratingSum = word[1][0]
        #    usage = word[1][1]
        #    newWord = Word()
         #   newWord.rating = ratingSum/usage
         #   newWord.value = word[0]
         #   newWord.votes = usage
         #   newWord.save()

        return render_to_response('Histogram.html',{'location' : location , 'beerType' : beerType , 'avbs' : avbs, 'description' : description , 'color':color}, context_instance=RequestContext(request))

