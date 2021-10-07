from django.shortcuts import get_object_or_404
from django.views import generic, View
from django.views.generic import edit
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.utils import timezone
from django.templatetags.static import static
from django.core import serializers
import json
from .models import Kit, Sample, Tag, Collection, Profile, Background
from .forms import ConfirmationForm, PasswordChangingForm
from django.template.loader import render_to_string

def sendInfoToModalDjango(self, request):
    self.object_list = self.get_queryset()
    if request.is_ajax():
        if(json.loads(request.body).get("post_data_1")):
            samples_selected_id = json.loads(request.body)["post_data_1"]
            samples_selected = Sample.objects.filter(id__in=samples_selected_id)
            url = []
            artist = []
            tag = []
            for sample in samples_selected:
                url.append(sample.file.url)
                artist.append(sample.user)
                if sample.tag :
                    tag.append(sample.tag)
                else :
                    defaultTagTmp = Tag.objects.create(name="no tag", color="transparent")
                    tag.append(defaultTagTmp)
                    Tag.objects.get(name="no tag").delete()
            ser_tag = serializers.serialize("json", tag,)
            ser_artist = serializers.serialize("json", artist,)
            ser_url = json.dumps(url)
            ser_samples_selected = serializers.serialize("json", samples_selected,)
            return JsonResponse({"samples_selected": ser_samples_selected, "samples_url": ser_url, "samples_artist": ser_artist, "samples_tag" : ser_tag}, status=200)
        elif(json.loads(request.body).get("post_data_2")):
            samples_selected_id = json.loads(request.body)["post_data_2"]
            samples_selected = Sample.objects.filter(id__in=samples_selected_id)
            for sample in samples_selected :
                if request.user not in sample.users.all():
                    sample.users.add(request.user)
            return JsonResponse({"type": "addToMySamples"}, status=200)
    else :
        self.samples_selected = None
        context = self.get_context_data()
        return  self.render_to_response(context)

class SampleListView(LoginRequiredMixin,generic.ListView):
    model = Sample
    macro = False 
    filter_name = False
    filter_tag = False
    filter_user = False
    length = None

    def post(self, request):
        return sendInfoToModalDjango(self, request)

    def get_queryset(self):
        q_objects=Q(isPublic=True)
        if ("filter_by_all") in self.request.GET:
            filter_by_all=self.request.GET['filter_by_all']
            if self.request.GET.get("filter_macro") == "on":
                self.macro = True
            else:
                self.macro = False
            if filter_by_all:
                if 'name' in self.request.GET.getlist("filter_selection"):
                    q_objects&=Q(name__icontains=filter_by_all)
                    self.filter_name = True
                else:
                    self.filter_name = False
                if 'artist' in self.request.GET.getlist("filter_selection"):
                    q_objects&=Q(user__username__icontains=filter_by_all)
                    self.filter_user = True
                else:
                    self.filter_user = False
                if 'tag' in self.request.GET.getlist("filter_selection"):
                    q_objects_tag=Q()
                    for tag in filter_by_all.split(" "):
                        q_objects_tag|=Q(tag__name__icontains=tag)
                    q_objects&=q_objects_tag
                    self.filter_tag = True
                else:
                    self.filter_tag = False
                if self.request.GET.getlist("filter_selection") == [] :
                    q_objects&=Q(name__icontains=filter_by_all)|Q(user__username__icontains=filter_by_all)
                    q_objects_tag = Q()
                    for tag in filter_by_all.split(" "):
                        q_objects_tag|=Q(tag__name__icontains=tag)
                    q_objects|=q_objects_tag
            queryset=super().get_queryset().filter(q_objects)
            self.length = queryset.count()
            return queryset
        else :
            self.length = None
            queryset=super().get_queryset().filter(q_objects)
            return queryset   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['collection_list'] = Collection.objects.filter(users__in=[self.request.user])
        context['macro'] = self.macro
        context['filter_name'] = self.filter_name
        context['filter_tag'] = self.filter_tag
        context['filter_user'] = self.filter_user
        context['length'] = self.length
        context["created"] = self.request.session.get("createdSample")
        self.request.session['createdSample'] = False
        return context 

class MySampleListView(LoginRequiredMixin,generic.ListView):
    model = Sample
    macro = False 
    template_name = "samples/my_sample_list.html"
    filter_name = False
    filter_tag = False
    filter_user = False
    length = None

    def post(self, request):
        self.object_list = self.get_queryset()
        if request.is_ajax():
            if(json.loads(request.body).get("post_data_1")):
                samples_selected_id = json.loads(request.body)["post_data_1"]
                samples_selected = Sample.objects.filter(id__in=samples_selected_id)
                url = []
                artist = []
                tag = []
                for sample in samples_selected:
                    url.append(sample.file.url)
                    artist.append(sample.user)
                    tag.append(list(sample.tag.values()))
                ser_tag = json.dumps(tag)
                ser_artist = serializers.serialize("json", artist,)
                ser_url = json.dumps(url)
                ser_samples_selected = serializers.serialize("json", samples_selected,)
                return JsonResponse({"samples_selected": ser_samples_selected, "samples_url": ser_url, "samples_artist": ser_artist, "samples_tag" : ser_tag}, status=200)
            elif(json.loads(request.body).get("post_data_2")):
                samples_selected_id = json.loads(request.body)["post_data_2"]
                samples_selected = Sample.objects.filter(id__in=samples_selected_id)
                for sample in samples_selected :
                    if request.user in sample.users.all():
                        sample.users.remove(request.user)
                        sample.save()
                data = {'sample_list': render_to_string('samples/sampleItems/sample_list_item.html', context=self.get_context_data()), "type": "deleteFromMySamples"}
                return JsonResponse(data)
            elif(json.loads(request.body).get("post_data_delete")):
                sample_selected_id = json.loads(request.body)["post_data_delete"]
                sample_selected = Sample.objects.filter(id=sample_selected_id)
                sample_selected.delete()
                data = {'sample_list': render_to_string('samples/sampleItems/sample_list_item.html', context=self.get_context_data()), "type": "deleteFromMySamples"}
                return JsonResponse(data)
        else :
            self.samples_selected = None
            return JsonResponse({}, status=200)

    def get_queryset(self):
        if ("filter_by_all") in self.request.GET:
            filter_by_all=self.request.GET['filter_by_all']
            if self.request.GET.get("filter_macro") == "on":
                self.macro = True
            else:
                self.macro = False
            filter_by_name=self.request.GET.get('filter_by_name')
            filter_by_user=self.request.GET.get('filter_by_user')
            filter_by_tag=self.request.GET.get('filter_by_tag')
            q_objects=Q()
            if filter_by_all:
                if filter_by_name:
                    q_objects&=Q(name__icontains=filter_by_all)
                    self.filter_name = True
                else:
                    self.filter_name = False
                if filter_by_user:
                    q_objects&=Q(user__username__icontains=filter_by_all)
                    self.filter_user = True
                else:
                    self.filter_user = False
                if filter_by_tag:
                    q_objects_tag=Q()
                    for tag in filter_by_all.split(" "):
                        q_objects_tag|=Q(tag__name__icontains=tag)
                    q_objects&=q_objects_tag
                    self.filter_tag = True
                else:
                    self.filter_tag = False
                if not(filter_by_name) and not(filter_by_tag) and not(filter_by_user) :
                    q_objects&=Q(name__icontains=filter_by_all)|Q(user__username__icontains=filter_by_all)
                    for tag in filter_by_all.split(" "):
                        q_objects|=Q(tag__name__icontains=tag)   
            q_objects&=Q(users__in=[self.request.user])
            queryset=super().get_queryset().filter(q_objects)
            self.length = queryset.count()
            return queryset
        else :
            self.length = None
            return Sample.objects.filter(users__in=[self.request.user])      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['collection_list'] = Collection.objects.filter(users__in=[self.request.user])
        context['macro'] = self.macro
        context['filter_name'] = self.filter_name
        context['filter_tag'] = self.filter_tag
        context['filter_user'] = self.filter_user
        context['length'] = self.length
        context["created"] = self.request.session.get("createdSample")
        context["path"] = self.request.path
        context["user"] = self.request.user
        context[self.get_context_object_name] = Sample.objects.filter(users__in=[self.request.user])
        self.request.session['createdSample'] = False
        return context     

class SampleCreateView(LoginRequiredMixin,edit.CreateView):
    model = Sample
    fields = ["name","file", "isPublic"]
    success_url = reverse_lazy('sample_list')
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        self.object = form.save()
        self.object.isItMacro()
        self.object.users.add(self.request.user)
        bgId = self.object.get_bgId_or_bg()
        self.object.background = Background.objects.get(id=bgId)
        self.object.save()
        if 'mycollections' in self.request.path :
            collection = get_object_or_404(Collection,id=self.kwargs["pk"])
            collection.samples.add(self.object)
            collection.save()
            self.success_url = reverse_lazy('my_collection_detail', kwargs={'pk': self.kwargs["pk"]})
        elif 'mysamples' in self.request.path:
            self.success_url = reverse_lazy('my_sample_list')
        elif 'recents' in self.request.path:
            self.success_url = reverse_lazy('recents')
        else:
            self.success_url = reverse_lazy('sample_list')
        self.request.session['createdSample'] = True
        return super().form_valid(form)

class SampleDetailView(LoginRequiredMixin,edit.CreateView):
    model = Sample
    template_name='samples/sample_detail.html'
    fields=['name','file']
    success_url=reverse_lazy('sample_detail')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['object']=self.get_object()
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        self.object = form.save()
        self.object.isItMacro()
        self.object.users.add(self.request.user)
        bgId = self.object.get_bgId_or_bg()
        self.object.background = Background.objects.get(id=bgId)
        self.object.save()
        if 'mysamples' in self.request.path:
            self.success_url = reverse_lazy('my_sample_detail', kwargs={'pk':self.object.id})
        elif 'recents' in self.request.path:
            self.success_url = reverse_lazy('recents_detail', kwargs={'pk':self.object.id})
        else:
            self.success_url = reverse_lazy('sample_detail', kwargs={'pk':self.object.id})
        return super().form_valid(form)
        
class SampleUpdateView(LoginRequiredMixin,edit.UpdateView):
    model = Sample
    fields = ["name", "isPublic", 'tag']
    success_url = reverse_lazy('my_sample_list')

    def form_valid(self, form):
        if "mycollections" in self.request.path:
            self.success_url = reverse_lazy('my_collection_detail', kwargs={'pk':self.kwargs["pkcol"]})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Update"
        context['tag_list'] = Tag.objects.all()
        return context
    
class SampleDeleteView(LoginRequiredMixin,generic.FormView):
    form_class = ConfirmationForm
    template_name = "samples/sample_delete.html"
    success_url = reverse_lazy('my_sample_list')

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        return Sample.objects.filter(pk__in=id_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] =self.get_object_list()
        return context

    def form_valid(self, form):
        for sample in self.get_object_list() :
            sample.users.remove(self.request.user)
            sample.save()
        return super().form_valid(form)


class SampleMultiView(View):

    success_url = reverse_lazy('sample_list')

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        path = self.request.path.split("/")
        object_list = Sample.objects.filter(pk__in=id_list)
        if 'mysamples' in self.request.path:
            self.success_url = reverse_lazy('my_sample_list')
        elif 'recents' in self.request.path:
            self.success_url = reverse_lazy('recents')
        elif 'mycollections' in self.request.path:
            self.success_url = reverse_lazy('my_collection_detail', kwargs={'pk': path[2]})
        elif 'collections' in self.request.path:
            self.success_url = reverse_lazy('collection_detail', kwargs={'pk': path[2]})
        else:
            self.success_url = reverse_lazy('sample_list')
        return object_list


class SampleAddToUser(LoginRequiredMixin,generic.FormView):
    form_class = ConfirmationForm
    template_name = "samples/sample_add_to_user.html"
    success_url = reverse_lazy('sample_list')

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        return Sample.objects.filter(pk__in=id_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] =self.get_object_list()
        return context

    def form_valid(self, form):
        for sample in self.get_object_list() :
            if self.request.user not in sample.users.all(): 
                sample.users.add(self.request.user)
                sample.save()
        path = self.request.path.split("/")
        if 'collection' in self.request.path :
            self.success_url = reverse_lazy("collection_detail", kwargs={'pk': path[2]})
        elif 'recents' in self.request.path :
            self.success_url = reverse_lazy("recents")
        else:
            self.success_url = reverse_lazy("sample_list")
        return super().form_valid(form)

class AddTagView(LoginRequiredMixin,SampleMultiView):

    def get(self, request, *args, **kwargs):
        tag = get_object_or_404(Tag,id=self.kwargs["tag"])
        for object in self.get_object_list():
            object.tag=tag
            object.save()
        return HttpResponseRedirect(self.success_url)


class ClearTagView(LoginRequiredMixin,SampleMultiView):

    def get(self, request, *args, **kwargs):
        for object in self.get_object_list():
            object.tag = None
            object.save()
        return HttpResponseRedirect(self.success_url)


class RecentView(LoginRequiredMixin, generic.ListView):
    model=Sample
    macro = False
    length = None
    filter_name = False
    filter_tag = False
    filter_user = False

    def post(self, request):
        return sendInfoToModalDjango(self, request)
    
    def get_queryset(self):
       
        if ("filter_by_all") in self.request.GET:
            filter_by_all=self.request.GET['filter_by_all']
            if self.request.GET.get("filter_macro") == "on":
                self.macro = True
            else:
                self.macro = False
            filter_by_name=self.request.GET.get('filter_by_name')
            filter_by_user=self.request.GET.get('filter_by_user')
            filter_by_tag=self.request.GET.get('filter_by_tag')
            q_objects=Q(isPublic=True)
            if filter_by_all:
                if filter_by_name:
                    q_objects&=Q(name__icontains=filter_by_all)
                    self.filter_name = True
                else:
                    self.filter_name = False
                if filter_by_user:
                    q_objects&=Q(user__username__icontains=filter_by_all)
                    self.filter_user = True
                else:
                    self.filter_user = False
                if filter_by_tag:
                    q_objects_tag=Q()
                    for tag in filter_by_all.split(" "):
                        q_objects_tag|=Q(tag__name__icontains=tag)
                    q_objects&=q_objects_tag
                    self.filter_tag = True
                else:
                    self.filter_tag = False
                if not(filter_by_name) and not(filter_by_tag) and not(filter_by_user) :
                    q_objects&=Q(name__icontains=filter_by_all)|Q(user__username__icontains=filter_by_all)
                    q_objects_tag = Q()
                    for tag in filter_by_all.split(" "):
                        q_objects_tag|=Q(tag__name__icontains=tag)
                    q_objects|=q_objects_tag
            q_objects&=Q(isRecent=True)
            queryset=super().get_queryset().filter(q_objects)
            self.length = queryset.count()
            return queryset
        else :
            self.length = None
            return Sample.objects.filter(created_date__lte=timezone.now(), isRecent=True, isPublic=True).order_by('-created_date')
    
    def get_context_data(self, **kwargs):
        sample_list=Sample.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        for sample in sample_list:
            sample.was_published_recently()
            sample.save()
        context = super().get_context_data(**kwargs)
        context['macro'] = self.macro
        context['filter_name'] = self.filter_name
        context['filter_tag'] = self.filter_tag
        context['filter_user'] = self.filter_user
        context['collection_list'] = Collection.objects.filter(users__in=[self.request.user])
        context['length'] = self.length
        context["created"] = self.request.session.get("createdSample")
        self.request.session['createdSample'] = False
        return context

class AddCollectionView(LoginRequiredMixin,SampleMultiView):

    def get(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection,id=self.kwargs["collection"])
        for object in self.get_object_list():
            if not object.isPublic and collection.isPublic:
                object.isPublic = True
                object.save()
            if self.request.user not in object.users.all():
                object.users.add(self.request.user)
                object.save()
            if object not in collection.samples.all() :
                collection.samples.add(object)
        collection.save()
        return HttpResponseRedirect(self.success_url)

class ClearCollectionView(LoginRequiredMixin,SampleMultiView):

    def get(self, request, *args, **kwargs):
        #get collection of user
        collection_list = Collection.objects.filter(user=self.request.user)
        for object in self.get_object_list():
            for collection in collection_list:
                collection.samples.remove(object)

        return HttpResponseRedirect(self.success_url)

class SwitchThemeView(LoginRequiredMixin,generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        theme=self.request.GET.get('theme')

        if theme=="dark":
            self.request.session['theme']=static('css/darkPalette.css')
            self.request.session['testTheme']=False
            self.request.session.modified=True
        else:
            self.request.session['theme']=static('css/lightPalette.css')
            self.request.session['testTheme']=True
            self.request.session.modified=True
        return self.request.GET.get('redirect')


class ProfileView(LoginRequiredMixin,generic.UpdateView):
    model=Profile
    template_name="samples/profile.html"
    fields=['bio', 'favMusicSoftware', 'musicStyle']

    def get_object(self, queryset=None):
        user = self.request.user
        #If User has no Profile, this will be created
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            Profile.create_user_profile(sender=user, instance=user, created=True)
            profile = Profile.objects.get(user=user)
            profile.save()
        return profile
    
    def get_success_url(self):
        redirect=self.request.POST.get('redirect')
        return redirect

class UpdateProfileImage(LoginRequiredMixin, generic.UpdateView):
    model=Profile
    fields=['image']

    def get_success_url(self):
        redirect=self.request.POST.get('redirect')
        return redirect

class UpdateUserInfo(LoginRequiredMixin, generic.UpdateView):
    model=User
    fields=['first_name','last_name','username','email']

    def get_success_url(self):
        redirect=self.request.POST.get('redirect')
        return redirect

class PasswordsChangeView(LoginRequiredMixin,PasswordChangeView):
    form_class = PasswordChangingForm
    template_name='registration/password_change_form.html'

    def get_success_url(self):
        redirect=self.request.POST.get('redirect')
        return redirect

class SidebarView(LoginRequiredMixin,generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if "menu" in self.request.session:
                menu = self.request.session.get('menu')
                if menu == 'small':
                    self.request.session['menu']='large'
                    self.request.session['menuSize']='250px'
                else :
                    self.request.session['menu']='small'
                    self.request.session['menuSize']='100px'
            else:
                self.request.session['menu']='large'
                self.request.session['menuSize']='250px'
            self.request.session.modified
            data={'menuSize':self.request.session.get('menuSize'), 'menu':self.request.session.get('menu')}
            return JsonResponse(data)

class SubMenuAPIView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if(json.loads(request.body).get("submenu1")):
                self.request.session['submenu1_state']='show'
            else:
                self.request.session['submenu1_state']=''
            if(json.loads(request.body).get("submenu2")):
                self.request.session['submenu2_state']='show'
            else:
                self.request.session['submenu2_state']=''
            self.request.session.modified
            return JsonResponse({'data':"ok"},status=200)
    

class GetKit(generic.DetailView):
    model=Kit

    def get(self, request, *args, **kwargs):
        kit = Kit.objects.get(pk=self.kwargs['pk'])
        samples = kit.sampleList.all()
        data = serializers.serialize('json', samples, fields=('name','file'))
        return JsonResponse({'samples':data}, status=200)

class CreateKitFromSample(LoginRequiredMixin,edit.CreateView):
    model=Kit
    fields=['sampleList']
    template_name='samples/sampleItems/form_create_kit_sample.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return JsonResponse({'kitId':self.object.id}, status=200)