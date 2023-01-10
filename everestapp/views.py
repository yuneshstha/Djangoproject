from django.views.generic import View, TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.urls import reverse, reverse_lazy

class ClientMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['latestnews'] = News.objects.all().order_by('-id')
        context['categories'] = Category.objects.all()
        context['comments'] = Comment.objects.all().order_by('-id')
        return context

class AdminRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = request.user
            if self.user.is_superuser and self.user.is_active:
                print("Admin Only Passed")
            else:
                return redirect("everestapp:adminlogin"+"?next=" + request.get_full_path())
        except Exception as e:
            print(e)
            return redirect("everestapp:adminlogin")
        return super().dispatch(request, *args, **kwargs)


class AdminLoginView(FormView):
    template_name = "adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("everestapp:clientnewscreate")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                username = user.username
                login(self.request, user)
            except Exception as e:
                print(e)
                return render(self.request, self.template_name, {"form": form, "error": "Invalid Credentials.."})
        else:
            return render(self.request, self.template_name, {"form": form, "error": "Invalid Credentials.."})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class AdminLogoutView(View):
    success_message = 'Logged out successfully'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect('everestapp:clienthome')
        else:
            raise Http404

class ClientHomeView(ClientMixin, TemplateView):
    template_name = "clienthome.html"

class ClientAboutView(TemplateView):
    template_name = "clientabout.html"

class ClientServiceView(TemplateView):
    template_name = "clientservice.html"

class ClientContactView(TemplateView):
    template_name = "clientcontact.html"


class ClientNewsListView(ClientMixin, ListView):
    template_name = "clientnewslist.html"
    model = News
    context_object_name = 'newslist'


class ClientNewsDetailView(ClientMixin, DetailView):
    template_name = 'clientnewsdetail.html'
    model = News
    context_object_name = 'newsdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.id = self.kwargs['pk']
        news = News.objects.get(id=self.id)
        viewcount = news.viewed + 1
        news.viewed = viewcount
        news.save()
        context['form'] = NewsCommentForm
        context['comments'] = Comment.objects.filter(post=news)
        return context


class ClientNewsCommentCreateView(ClientMixin, FormView):
    template_name = 'newsdetail.html'
    form_class = NewsCommentForm
    success_url = '/'
    success_message = 'Thank you for creating comment here. '

    def dispatch(self, *args, **kwargs):
        self.id = self.kwargs['pk']
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.comment = form.cleaned_data['comment']
        self.commentername = form.cleaned_data['commentername']
        self.news = News.objects.get(id=self.id)
        Comment.objects.create(post=self.news, comment=self.comment,
                               commentername=self.commentername)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        # url = '/news/' + str(self.id)
        # return url
        return reverse('everestapp:clientnewsdetail', kwargs={
            'pk': self.kwargs['pk'],
        })


class ClientNewsCreateView(AdminRequiredMixin, CreateView):
    template_name = "clientnewscreate.html"
    form_class = ClientNewsCreateForm
    model = News
    success_url = reverse_lazy("everestapp:clienthome")

class ClientNewsUpdateView(UpdateView):
    template_name = "clientnewscreate.html"
    form_class = ClientNewsCreateForm
    model = News
    success_url = reverse_lazy("everestapp:clienthome")

class ClientNewsDeleteView(DeleteView):
    template_name = "clientnewsdelete.html"
    model = News
    context_object_name = "news"
    success_url = reverse_lazy("everestapp:clienthome")