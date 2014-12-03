import sys
import numpy
from app.models import Comment
from app.models import Location
from app.models import AbvsRange
from app.models import BeerStyle
from app.models import StyleData
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

def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

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

    return render_to_response('list.html', {'commentList' : commentList, 'form' : form }, context_instance=RequestContext(request))


def map(request):
    return render_to_response('map.html',{}, context_instance=RequestContext(request))


def colors(request):
    colorList = Color.objects.all().order_by('-rating')

    return render_to_response('colors.html',{'colorList' : colorList}, context_instance=RequestContext(request))


def prediction(request):

    locations = Location.objects.all()
    abvsRanges = AbvsRange.objects.all()
    beerStyle = BeerStyle.objects.all()

    return render_to_response('prediction.html',{'locationList': locations , 'abvsRangesList': abvsRanges , 'beerStyleList' : beerStyle}, context_instance=RequestContext(request))


def getPrediction(request):

    if request.method == 'POST':
        location = request.POST.get('location')
        beerStyle = request.POST.get('beerStyle')
        abvRangeId = request.POST.get('abvs')
        description = request.POST.get('description')
        color = request.POST.get('color')

        abvData = Abvs.objects.get(location__exact=location, abvsrange__exact=abvRangeId)
        abvLng = numpy.array(abvData.lngcoord, dtype=str)
        abvLat = numpy.array(abvData.latcoord, dtype=object)
        abvRatings = numpy.array(abvData.rating, dtype=object)
        styleData = StyleData.objects.get(location__exact=location, beerStyle__exact=beerStyle)
        styleLng = numpy.array(styleData.lngcoord, dtype=object)
        #styleLng = styleLng.view(numpy.float64)
        styleLat = numpy.array(styleData.latcoord, dtype=object)
        styleRatings = numpy.array(styleData.rating, dtype=object)

        print abvLng[0]
        print type(abvLng)






        #getWords()

        return render_to_response('Histogram.html',{'location' : location , 'beerStyle' : beerStyle , 'abvs' : abvRangeId, 'description' : description , 'color':color}, context_instance=RequestContext(request))


def getWords():

    try:
        keywordsFile = open('C:/keywords.json', 'rb')
    except:
        print 'Keywords.json not found.'
        sys.exit()

    try:
        f = keywordsFile.read()
        keywordsDict = jpickle.decode(f)
    except:
        keywordsDict = []
        print 'Keywords list corrupted'
        sys.exit()
    keywordsFile.close()

    #Sorted by average rating
    SortedByRating = {}
    SortedByRating['keywords'] = []
    SortedByRating['ratings'] = []
    SortedByRating['usage'] = []
    for word in sorted(keywordsDict.items()[10400:], key=lambda k: (k[1][0] / k[1][1]), reverse=True):
        try:
            ratingSum = word[1][0]
            usage = word[1][1]
            newWord = Word()
            newWord.rating = ratingSum/usage
            newWord.value = word[0]
            newWord.votes = usage
            newWord.save()
        except Exception,e:
            HttpResponse("ratingsum: " +word[1][0] + " usage:" + word[1][1] + "value:" + word[0] + str(e) )
