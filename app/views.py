from app.models import Comment
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from app.forms import CommentForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden

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

def addNewEntry(request):

    return render_to_response('list.html',{}, context_instance=RequestContext(request))