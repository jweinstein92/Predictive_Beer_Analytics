import sys
import numpy
import cStringIO
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
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
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

    return render_to_response('description.html',{'topList' : topList, 'bottomList' : bottomList}, context_instance=RequestContext(request))

def getDescription(request):

    if request.method == 'POST' and request.POST.get('qry') != "":
        query = request.POST.get('qry')

        resultList = Word.objects.filter(Q(value__icontains=query)).order_by('-rating')[:5]

    return render_to_response('descriptionresult.html',{'resultList' : resultList }, context_instance=RequestContext(request))

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

        abvData = Abvs.objects.get(location=location, abvsrange=abvRangeId)
        styleData = StyleData.objects.get(location=location, beerStyle=beerStyle)

        # The data stored in the database returns as unicode. must make into string
        # and then into ndarray
        abvLng = createNdArray(abvData.lngcoord.encode('utf8'))
        abvLat = createNdArray(abvData.latcoord.encode('utf8'))
        abvRatings = createNdArray(abvData.rating.encode('utf8'))

        styleLng = createNdArray(styleData.lngcoord.encode('utf8'))
        styleLat = createNdArray(styleData.latcoord.encode('utf8'))
        styleRatings = createNdArray(styleData.rating.encode('utf8'))

        avgLng = (abvLng + styleLng) / 2
        avgLat = (abvLat + styleLat) / 2
        avgRatings = (abvRatings + styleRatings) / 2
        if (location == '1'):
            map = createUSMap(avgLat, avgLng, avgRatings)
        else:
            map = createEUMap(avgLat, avgLng, avgRatings)
        # Encode image to png in base64
        io = cStringIO.StringIO()
        plt.savefig(io, format='png')
        plt.close()
        data = io.getvalue().encode('base64')
        #getWords()

        # print sio.getvalue().encode("base64").strip()
        return render_to_response('Histogram.html',{'location' : location , 'beerStyle' : beerStyle , 'abvs' : abvRangeId, 'description' : description , 'color':color, 'map':data}, context_instance=RequestContext(request))


def createNdArray(arrayString):
    arrayString = arrayString[1:len(arrayString)-1]
    arrayString = arrayString.split(',')
    nd = []
    for num in arrayString:
        num = num.strip()
        if num[0] == '[':
            num = num[1:]
            newArray = [float(num)]
        elif num[len(num)-1] == ']':
            num = num[:len(num)-1]
            newArray.append(float(num))
            nd.append(newArray)
            newArray = []
        else:
            newArray.append(float(num))
    ndArray = np.array(nd)
    return ndArray


def createUSMap(lats, lngs, ratings):
    usLat = [38, 22, 48]
    usLng = [-97, -125, -59]
    parallels = [30, 40]
    meridians = [280, 270, 260, 250, 240]
    # create polar stereographic Basemap instance.
    m = Basemap(projection='stere', lat_0=usLat[0], lon_0=usLng[0],
            llcrnrlat=usLat[1], urcrnrlat=usLat[2],
            llcrnrlon=usLng[1], urcrnrlon=usLng[2],
            rsphere=6371200, resolution='l', area_thresh=10000)
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    # draw parallels.
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    # draw meridians
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

    # overlay the averages histogram over map
    plt.pcolormesh(lngs, lats, ratings, vmin=0, vmax=5)
    plt.colorbar(orientation='horizontal')
    return m


def createEUMap(lats, lngs, ratings):
    euLat = [51, 27, 71]
    euLng = [20, -16, 45]
    parallels = [30, 40, 50, 60, 70]
    meridians = [350, 0, 10, 20, 30, 40]
    # create polar stereographic Basemap instance.
    m = Basemap(projection='stere', lat_0=euLat[0], lon_0=euLng[0],
            llcrnrlat=euLat[1], urcrnrlat=euLat[2],
            llcrnrlon=euLng[1], urcrnrlon=euLng[2],
            rsphere=6371200, resolution='l', area_thresh=10000)
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawcountries()

    # draw parallels.
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    # draw meridians
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

    # overlay the averages histogram over map
    plt.pcolormesh(lngs, lats, ratings, vmin=0, vmax=5)
    plt.colorbar(orientation='horizontal')
    return m


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
