from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from .models import Category, Topic, Reply
from .forms import ReplyForm, TopicForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.contrib import messages


class ForumHome(ListView):
    model = Category
    template_name = 'forum/home.html'

    # Displaying all category, it's count, latest topic and latest reply

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        table_data = []
        for category in categories:
            categoryObject = Topic.objects.filter(category=category)
            replies = 0
            for topic in categoryObject:
                replies = replies + Reply.objects.filter(topic=topic).count()

            data = {
                'category': category,
                'count': categoryObject.count(),
                'latest': categoryObject.first(),
                'replies': replies,
            }
            table_data.append(data)

        context['table_data'] = table_data
        # Recent data
        context['recent_data'] = Topic.objects.all()[:7]
        return context


# All topic list according to a category
class CategoryTopics(ListView):
    template_name = 'forum/topic_list.html'
    context_object_name = 'topic_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, ~Q(name='Trash'), name=self.kwargs['category'])

        data = Topic.objects.filter(
            category=self.category)

        # For filtering topics in ascending and descending order
        if(self.request.GET.get('order-by') != None):
            if self.request.GET.get('order') == 'asc':
                data = data.order_by(self.request.GET.get('order-by'))
            else:
                data = data.order_by('-' + self.request.GET.get('order-by'))

        result = []

        for item in data:
            replies = Reply.objects.filter(topic=item)

            last_username = replies.last().user.username
            last_date = replies.last().published_date
            last_image = replies.last().user.profile.image.url

            result.append({
                'topic': item,
                'replies': replies.count(),
                'last_username': last_username,
                'last_date': last_date,
                'last_image': last_image
            })
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context

    # Moderator actions
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and 'topic_id' in request.POST:
            topic_id = request.POST.get('topic_id')
            currentTopic = Topic.objects.get(id=topic_id)
            if request.POST.get('type') == 'delete':
                deletedCategory = Category.objects.get(name='Trash')
                currentTopic.category = deletedCategory
                currentTopic.save()
                return JsonResponse({'success': True})
            elif request.POST.get('type') == 'pin':
                if currentTopic.is_pinned == True:
                    currentTopic.is_pinned = False
                    currentTopic.save()
                    return JsonResponse({'is_pinned': False})
                else:
                    currentTopic.is_pinned = True
                    currentTopic.save()
                    return JsonResponse({'is_pinned': True})
            elif request.POST.get('type') == 'lock':
                if currentTopic.is_locked == True:
                    currentTopic.is_locked = False
                    currentTopic.save()
                    return JsonResponse({'is_locked': False})
                else:
                    currentTopic.is_locked = True
                    currentTopic.save()
                    return JsonResponse({'is_locked': True})


# Single Discussion thread
class SingleTopic(ListView):
    template_name = 'forum/single_topic.html'
    form = ReplyForm()
    context_object_name = 'reply_list'
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        self.topic = get_object_or_404(
            Topic, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        replies = Reply.objects.filter(
            topic=self.topic)
        result = []
        already_liked = []
        for reply in replies:
            liked = False
            flagged = False
            if reply.likes.filter(id=self.request.user.id).exists():
                liked = True
            if reply.flags.filter(id=self.request.user.id).exists():
                flagged = True
            result.append({
                'reply': reply,
                'liked': liked,
                'flagged': flagged,
            })

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['category'] = self.topic.category.name
        context['title'] = self.topic.title
        context['topic_id'] = self.kwargs['slug']
        context['is_locked'] = self.topic.is_locked
        return context

    # All discussion thread actions
    def post(self, request, *args, **kwargs):

        if request.is_ajax() and request.POST.get('operation') == 'like_submit':
            reply_id = request.POST.get('content_id', None)
            reply = get_object_or_404(Reply, pk=reply_id)
            if reply.likes.filter(id=request.user.id):
                reply.likes.remove(request.user)
                liked = False
            else:
                reply.likes.add(request.user)
                liked = True

            data = {"liked": liked, "reply_id": reply_id,
                    "likes": reply.total_likes}
            return JsonResponse(data)
        elif request.is_ajax() and request.POST.get('operation') == 'flag_submit':
            reply_id = request.POST.get('content_id', None)
            reply = get_object_or_404(Reply, pk=reply_id)
            reply.flags.add(request.user)
            data = {
                "reply_id": reply_id,
                "total_flags": reply.total_flags,
            }
            return JsonResponse(data)

        elif request.is_ajax() and request.POST.get('operation') == 'delete_reply':
            reply_id = request.POST.get('content_id', None)
            reply = get_object_or_404(Reply, pk=reply_id)
            reply.is_deleted = True
            reply.save()
            return JsonResponse({'success': True})

        self.form = ReplyForm(request.POST)
        if self.form.is_valid():
            self.form.instance.user = request.user
            self.form.instance.topic = self.topic
            self.form.save()
            return redirect(self.topic)
        else:
            messages.warning(
                request, self.form.errors['content'][0])
            return redirect(self.topic)


# Creating topic view
@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreateTopic(View):
    form_class = TopicForm
    template_name = 'forum/create_topic.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newTopic = Topic(title=form.cleaned_data['title'],
                             category=form.cleaned_data['category'], user=request.user)
            newTopic.save()
            newReply = Reply(user=request.user, topic=newTopic,
                             content=form.cleaned_data['content'])
            newReply.save()

            return redirect(newTopic)
        return render(request, self.template_name, {'form': form})


# Edit reply view
@login_required(login_url='/login')
def editReply(request, id):
    replyEdited = get_object_or_404(
        Reply, id=id, user=request.user, is_deleted=False)
    form = ReplyForm(instance=replyEdited)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=replyEdited)
        if form.is_valid():
            form.save()
            return redirect(replyEdited.topic)

    context = {
        'form': form
    }
    return render(request, 'forum/edit_reply.html', context)


# Search field in the forum
def search(request):
    if 'query' in request.GET and request.is_ajax():
        users = User.objects.filter(
            username__startswith=request.GET.get('query'))
        result = []
        id = 1
        for user in users:
            result.append({'id': id, 'name': user.username,
                           'iconSrc': user.profile.image.url,
                           'userSrc': f'/profile/{user.username}'
                           })
            id += 1

        return JsonResponse(result, safe=False)

    elif 'term' in request.GET and request.is_ajax():
        data = []
        topics = Topic.objects.filter(title__icontains=request.GET.get('term'))
        users = User.objects.filter(
            username__icontains=request.GET.get('term'))
        for item in topics:
            data.append(item.title)
        for item in users:
            data.append(item.username)
        return JsonResponse(data, safe=False)
    elif 'category' in request.GET:
        if request.GET['category'] == 'topic':
            topics = Topic.objects.filter(
                title__icontains=request.GET.get('input'))
            return render(request, 'forum/search.html', {'data': topics, 'type': 'topic'})
        else:
            users = User.objects.filter(
                username__icontains=request.GET.get('input'))
            return render(request, 'forum/search.html', {'data': users, 'type': 'user'})

    return render(request, 'forum/search.html')
