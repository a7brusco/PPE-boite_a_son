from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic import edit
from .models import Sample, Tag, Collection, Kit
from .forms import ConfirmationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Q
import json
from django.template.loader import render_to_string


class CollectionListView(LoginRequiredMixin,generic.ListView):
    model = Collection
    filter_name = False
    filter_user = False
    length = None

    def post(self, request):
        self.object_list = self.get_queryset()
        if request.is_ajax():
            if(json.loads(request.body).get("post_data_1")):
                collections_selected_id = json.loads(request.body)["post_data_1"]
                collections_selected = Collection.objects.filter(id__in=collections_selected_id)
                artist = []
                for collection in collections_selected:
                    artist.append(collection.user)
                ser_artist = serializers.serialize("json", artist,)
                ser_collections_selected = serializers.serialize("json", collections_selected,)
                return JsonResponse({"collections_selected": ser_collections_selected, "collections_artist": ser_artist}, status=200)
            elif(json.loads(request.body).get("post_data_2")):
                collections_selected_id = json.loads(request.body)["post_data_2"]
                collections_selected = Collection.objects.filter(id__in=collections_selected_id)
                for collection in collections_selected :
                    if request.user not in collection.users.all():
                        collection.users.add(request.user)
                return JsonResponse({}, status=200)
            else :
                self.samples_selected = None
                context = self.get_context_data()
                return  self.render_to_response(context)
        else :
            self.samples_selected = None
            context = self.get_context_data()
            return  self.render_to_response(context)

    def get_queryset(self):
        q_objects=Q(isPublic=True)
        if ("filter_by_all") in self.request.GET:
            filter_by_all=self.request.GET['filter_by_all']
            filter_by_name=self.request.GET.get('filter_by_name')
            filter_by_user=self.request.GET.get('filter_by_user')
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
                if not(filter_by_name) and not(filter_by_user) :
                    q_objects&=Q(name__icontains=filter_by_all)|Q(user__username__icontains=filter_by_all)
            queryset=super().get_queryset().filter(q_objects)
            self.length = queryset.count()
            return queryset
        else :
            self.length = None
            queryset=super().get_queryset().filter(q_objects)
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_name'] = self.filter_name
        context['filter_user'] = self.filter_user
        context['length'] = self.length
        context["created"] = self.request.session.get("createdCollection")
        self.request.session['createdCollection'] = False
        return context     

class MyCollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = "samples/mycollection_list.html"
    filter_name = False
    filter_user = False
    length = None

    def post(self, request):
        self.object_list = self.get_queryset()
        if request.is_ajax():
            if(json.loads(request.body).get("post_data_1")):
                collections_selected_id = json.loads(request.body)["post_data_1"]
                collections_selected = Collection.objects.filter(id__in=collections_selected_id)
                artist = []
                for collection in collections_selected:
                    artist.append(collection.user)
                ser_artist = serializers.serialize("json", artist,)
                ser_collections_selected = serializers.serialize("json", collections_selected,)
                return JsonResponse({"collections_selected": ser_collections_selected, "collections_artist": ser_artist}, status=200)
            elif(json.loads(request.body).get("post_data_2")):
                collections_selected_id = json.loads(request.body)["post_data_2"]
                collections_selected = Collection.objects.filter(id__in=collections_selected_id)
                for collection in collections_selected :
                    if request.user in collection.users.all():
                        collection.users.remove(request.user)
                        collection.save()
                data = {'collection_list': render_to_string('samples/sampleItems/collection_list_item.html', context=self.get_context_data()), "type": "deleteFromMyCollections"}
                return JsonResponse(data)
            elif(json.loads(request.body).get("post_data_delete")):
                collection_selected_id = json.loads(request.body)["post_data_delete"]
                collection_selected = Collection.objects.filter(id=collection_selected_id)
                collection_selected.delete()
                data = {'collection_list': render_to_string('samples/sampleItems/collection_list_item.html', context=self.get_context_data()), "type": "deleteFromMyCollections"}
                return JsonResponse(data)
            else :
                self.samples_selected = None
                return  JsonResponse()
        else :
            self.samples_selected = None
            return  JsonResponse()


    def get_queryset(self):
        if ("filter_by_all") in self.request.GET:
            filter_by_all=self.request.GET['filter_by_all']
            filter_by_name=self.request.GET.get('filter_by_name')
            filter_by_user=self.request.GET.get('filter_by_user')
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
                if not(filter_by_name) and not(filter_by_user) :
                    q_objects&=Q(name__icontains=filter_by_all)|Q(user__username__icontains=filter_by_all)
            q_objects&=Q(users__in=[self.request.user])
            queryset=super().get_queryset().filter(q_objects)
            self.length = queryset.count()
            return queryset
        else :
            self.length = None
            return Collection.objects.filter(users__in=[self.request.user])      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_name'] = self.filter_name
        context['filter_user'] = self.filter_user
        context['length'] = self.length
        context["created"] = self.request.session.get("createdCollection")
        context["user"] = self.request.user
        context["path"] = self.request.path
        context["allSamples"] = Sample.objects.all()
        self.request.session['createdCollection'] = False
        return context     

class CollectionCreateView(LoginRequiredMixin,edit.CreateView):
    model = Collection
    fields = ["name","description", "isPublic"]
    success_url = reverse_lazy('collection_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.object.users.add(self.request.user)
        if 'mycollections' in self.request.path : 
            self.success_url = reverse_lazy('my_collection_list')
        else:
            self.success_url = reverse_lazy('collection_list')
        self.request.session['createdCollection'] = True
        return super().form_valid(form)
    

class CollectionUpdateView(LoginRequiredMixin,edit.UpdateView):
    model = Collection
    fields = ["name","description","isPublic"]
    success_url = reverse_lazy('my_collection_list')
    template_name='samples/collection_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if(form.instance.isPublic):
            for i,sample in enumerate(self.object.samples.all()):
                sample.isPublic = True
                sample.save()
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Update"
        return context

class UpdateCollectionImage(LoginRequiredMixin, generic.UpdateView):
    model=Collection
    fields=['image']

    def get_success_url(self):
        redirect=self.request.POST.get('redirect')
        return redirect

class CollectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Collection
    template_name = "samples/collection_detail.html"
    filter_name = False
    filter_tag = False
    filter_user = False
    object_list = Sample.objects.filter(isPublic=True)
    length = None

    def get_queryset(self):
        sample_list = []
        if ("filter_by_all") in self.request.GET:
            filter_by_all=self.request.GET['filter_by_all']
            if self.request.GET.get("filter_macro") == "on":
                self.macro = True
            else:
                self.macro = False
            filter_by_name=self.request.GET.get('filter_by_name')
            filter_by_user=self.request.GET.get('filter_by_user')
            filter_by_tags=self.request.GET.get('filter_by_tags')
            if filter_by_all:
                if filter_by_name:  
                    collection = Collection.objects.filter(id=self.kwargs["pk"], samples__name__icontains=filter_by_all)
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
                    self.filter_name = True
                else:
                    self.filter_name = False
                if filter_by_user:
                    collection = Collection.objects.filter(id=self.kwargs["pk"], samples__user__username__icontains=filter_by_all)
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
                    self.filter_user = True
                else:
                    self.filter_user = False
                if filter_by_tags:
                    collection = Collection.objects.filter(id=self.kwargs["pk"], samples__tags__name__icontains=filter_by_all)
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
                    self.filter_tag = True
                else:
                    self.filter_tag = False
                if not(filter_by_name) and not(filter_by_tags) and not(filter_by_user) :
                    collection = (Collection.objects.filter(id=self.kwargs["pk"], samples__name__icontains=filter_by_all)|Collection.objects.filter(id=self.kwargs["pk"], samples__user__username__icontains=filter_by_all)|Collection.objects.filter(id=self.kwargs["pk"], samples__tags__name__icontains=filter_by_all))
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
            else:
                collection = Collection.objects.filter(id=self.kwargs["pk"])
                for sample in collection.values("samples"):
                    sample_list.append(sample["samples"])
            self.object_list = Sample.objects.filter(id__in=sample_list, isPublic=True)
            self.length = len(self.object_list)
            queryset=super().get_queryset()
            return queryset
        else :
            collection = Collection.objects.get(id=self.kwargs["pk"])
            self.object_list = collection.samples.filter(isPublic=True)
            queryset=super().get_queryset()
            self.length = None
            return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_list'] = Collection.objects.filter(users__in=[self.request.user])
        context['object_list'] = self.object_list
        context['filter_name'] = self.filter_name
        context['filter_tag'] = self.filter_tag
        context['filter_user'] = self.filter_user
        context['length'] = self.length
        return context 

class MyCollectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Collection
    template_name = "samples/my_collection_detail.html"
    filter_name = False
    filter_tag = False
    filter_user = False
    object_list = Sample.objects.all()
    length = None

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if(json.loads(request.body).get("post_data_delete")):
                sample_selected_id = json.loads(request.body)["post_data_delete"]
                sample_selected = Sample.objects.filter(id=sample_selected_id)
                sample_selected.delete()
                self.get_queryset()
                self.object = self.get_object()
                data = {'sample_list': render_to_string('samples/sampleItems/sample_list_item.html', context=self.get_context_data()), "type": "deleteFromMySamples"}
                return JsonResponse(data)
        else :
            return JsonResponse({}, status=200)

    def get_queryset(self):
        sample_list = []
        if ("filter_by_all") in self.request.GET:
            filter_by_all=self.request.GET['filter_by_all']
            if self.request.GET.get("filter_macro") == "on":
                self.macro = True
            else:
                self.macro = False
            filter_by_name=self.request.GET.get('filter_by_name')
            filter_by_user=self.request.GET.get('filter_by_user')
            filter_by_tags=self.request.GET.get('filter_by_tags')
            if filter_by_all:
                if filter_by_name:  
                    collection = Collection.objects.filter(id=self.kwargs["pk"], samples__name__icontains=filter_by_all)
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
                    self.filter_name = True
                else:
                    self.filter_name = False
                if filter_by_user:
                    collection = Collection.objects.filter(id=self.kwargs["pk"], samples__user__username__icontains=filter_by_all)
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
                    self.filter_user = True
                else:
                    self.filter_user = False
                if filter_by_tags:
                    collection = Collection.objects.filter(id=self.kwargs["pk"], samples__tags__name__icontains=filter_by_all)
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
                    self.filter_tag = True
                else:
                    self.filter_tag = False
                if not(filter_by_name) and not(filter_by_tags) and not(filter_by_user) :
                    collection = (Collection.objects.filter(id=self.kwargs["pk"], samples__name__icontains=filter_by_all)|Collection.objects.filter(id=self.kwargs["pk"], samples__user__username__icontains=filter_by_all)|Collection.objects.filter(id=self.kwargs["pk"], samples__tags__name__icontains=filter_by_all))
                    for sample in collection.values("samples"):
                        sample_list.append(sample["samples"])
            else:
                collection = Collection.objects.filter(id=self.kwargs["pk"])
                for sample in collection.values("samples"):
                    sample_list.append(sample["samples"])
            self.object_list = Sample.objects.filter(id__in=sample_list)
            self.length = len(self.object_list)
            queryset=super().get_queryset()
            return queryset
        else :
            collection = Collection.objects.get(id=self.kwargs["pk"])
            self.object_list = collection.samples.all()
            self.length = None
            queryset=super().get_queryset()
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.object
        context['tag_list'] = Tag.objects.all()
        context['collection_list'] = Collection.objects.filter(users__in=[self.request.user])
        context['object_list'] = self.object_list
        context['filter_name'] = self.filter_name
        context['filter_tag'] = self.filter_tag
        context['filter_user'] = self.filter_user
        context['length'] = self.length
        return context 


class CollectionAddSampleView(LoginRequiredMixin,View):

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        object_list = Sample.objects.filter(pk__in=id_list)
        return object_list

    def get(self, request, *args, **kwargs):

        collection = get_object_or_404(Collection,id=self.kwargs["collection"])
        collection.samples.clear()
        for object in self.get_object_list():
            collection.samples.add(object)
        return HttpResponseRedirect(reverse_lazy("collection_detail",kwargs={'pk':collection.pk}))


class CollectionDeleteView(LoginRequiredMixin,generic.FormView):
    form_class = ConfirmationForm
    template_name = "samples/collection_delete.html"
    success_url = reverse_lazy('collection_list')

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        return Collection.objects.filter(pk__in=id_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] =self.get_object_list()
        return context

    def form_valid(self, form):
        for collection in self.get_object_list() :
            collection.users.remove(self.request.user)
            collection.save()
        if 'mycollections' in self.request.path : 
            self.success_url = reverse_lazy('my_collection_list')
        else:
            self.success_url = reverse_lazy('collection_list')
        return super().form_valid(form)

class CollectionAddToUser(LoginRequiredMixin,generic.FormView):
    form_class = ConfirmationForm
    template_name = "samples/collection_add_to_user.html"
    success_url = reverse_lazy('collection_list')

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        return Collection.objects.filter(pk__in=id_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] =self.get_object_list()
        return context

    def form_valid(self, form):
        for collection in self.get_object_list() :
            if self.request.user not in collection.users.all(): 
                collection.users.add(self.request.user)
                collection.save()
                for sample in collection.samples.all():
                    if self.request.user not in sample.users.all():
                        sample.users.add(self.request.user)
                        sample.save()
        return super().form_valid(form)

class CollectionMultiView(View):

    success_url = reverse_lazy('my_collection_list')

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        object_list = Collection.objects.filter(pk__in=id_list)
        return object_list

class MyCollectionsSampleDeleteView(LoginRequiredMixin,generic.FormView):
    form_class = ConfirmationForm
    template_name = "samples/sample_delete.html"

    def get_object_list(self):
        id_list = self.request.GET["ids"].split(",")
        return Sample.objects.filter(pk__in=id_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] =self.get_object_list()
        return context

    def form_valid(self, form):
        collection = Collection.objects.get(id=self.request.path.split("/")[2])
        for sample in self.get_object_list() :
            sample.users.remove(self.request.user)
            collection.samples.remove(sample)
            sample.save()
            collection.save()
        self.success_url = reverse_lazy('my_collection_detail',kwargs={'pk':collection.id})
        return super().form_valid(form)


class CreateKitFromColl(LoginRequiredMixin,edit.CreateView):
    model=Kit
    fields=['sampleList']
    template_name='samples/sampleItems/form_create_kit_coll.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return JsonResponse({'kitId':self.object.id}, status=200)

# API
class CollectionAPIListView(LoginRequiredMixin,View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            collections_selected_id = json.loads(request.body)["collecId"]
            collections_selected = Collection.objects.filter(id__in=collections_selected_id)
            listOfSamples = []
            for collection in collections_selected:
                listOfId=[]
                samples = collection.samples.all()
                for sample in samples:
                    listOfId.append(sample.id)
                listOfSamples.append(listOfId)
            jsondata = self.listUnion(listOfSamples)
            return JsonResponse({'listOfId':jsondata}, status=200)
    
    def listUnion(self,listOflist):
        final_list = []
        for listItem in listOflist:
            final_list = list(set().union(final_list,listItem))
        return final_list