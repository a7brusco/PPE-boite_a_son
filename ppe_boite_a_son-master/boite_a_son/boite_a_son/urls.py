"""boite_a_son URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from samples.collection_views import *
from samples.sample_views import *
from samples.project_views import *
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('samples/', SampleListView.as_view(), name='sample_list'),
    path('samples/addToUser', SampleAddToUser.as_view(), name='sample_add_to_user'),
    path('mysamples/', MySampleListView.as_view(), name='my_sample_list'),
    path('samples/create', SampleCreateView.as_view(), name='sample_create'),
    path('mysamples/create', SampleCreateView.as_view(), name='mysample_create'),
    path('samples/detail/<int:pk>/', SampleDetailView.as_view(), name='sample_detail'),
    path('mysamples/detail/<int:pk>/', SampleDetailView.as_view(), name='my_sample_detail'),
    path('mysamples/update/<int:pk>/', SampleUpdateView.as_view(), name='mysample_update'),
    path('mysamples/delete', SampleDeleteView.as_view(), name='sample_delete'),
    path('samples/addtag/<int:tag>', AddTagView.as_view(), name='addtag'),
    path('mysamples/addtag/<int:tag>', AddTagView.as_view(), name='addtagfrommysamples'),
    path('mysamples/cleartag', ClearTagView.as_view(), name='cleartag'),
    path('samples/addcollection/<int:collection>', AddCollectionView.as_view(), name='addcollection'),
    path('mysamples/addcollection/<int:collection>', AddCollectionView.as_view(), name='addcollectionfrommysamples'),
    path('samples/clearcollection', ClearCollectionView.as_view(), name='clearcollection'),
    path('mysamples/clearcollection', ClearCollectionView.as_view(), name='mysamplesclearcollection'),
    path('collections/', CollectionListView.as_view(), name='collection_list'),
    path('collections/addToUser', CollectionAddToUser.as_view(), name='collection_add_to_user'),
    path('collections/create', CollectionCreateView.as_view(), name='collection_create'),
    path('collections/delete', CollectionDeleteView.as_view(), name='collection_delete'),
    path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collection_detail'),
    path('collections/<int:pk>/create', SampleCreateView.as_view(), name='collection_create_sample'),
    path('collections/<int:pk>/addToUser', SampleAddToUser.as_view(), name='collection_sample_add_to_user'),
    path('collections/<int:pk>/addcollection/<int:collection>', AddCollectionView.as_view(), name='add_collection_from_current_collection'),
    path('mycollections/', MyCollectionListView.as_view(), name='my_collection_list'),
    path('mycollections/create', CollectionCreateView.as_view(), name='my_collection_create'),
    path('mycollections/delete', CollectionDeleteView.as_view(), name='my_collection_delete'),
    path('mycollections/<int:pk>/', MyCollectionDetailView.as_view(), name='my_collection_detail'),
    path('mycollections/<int:pk>/update', CollectionUpdateView.as_view(), name='my_collection_update'), 
    path('mycollections/<int:pk>/delete', MyCollectionsSampleDeleteView.as_view(), name='my_collections_sample_delete'),
    path('mycollections/<int:pk>/addtag/<int:tag>', AddTagView.as_view(), name='my_collections_sample_addtag'),
    path('mycollections/<int:pk>/createSample', SampleCreateView.as_view(), name='my_collections_sample_addsample'),
    path('mycollections/<int:pk>/addcollection/<int:collection>', AddCollectionView.as_view(), name='add_collection_from_my_current_collection'),
    path('mycollections/<int:pk>/clearcollection', ClearCollectionView.as_view(), name='mycollectionssamplesclearcollection'),
    path('mycollections/<int:pk>/cleartag', ClearTagView.as_view(), name='mycollectionsamplecleartag'),
    path('mycollections/<int:pkcol>/update/<int:pk>/', SampleUpdateView.as_view(), name='my_collection_sample_update'),
    path('mycollections/<int:pkcol>/detail/<int:pk>/', SampleDetailView.as_view(), name='my_collection_sample_detail'),
    path('recents/', RecentView.as_view(), name='recents'),
    path('recents/create', SampleCreateView.as_view(), name='recents_create'),
    path('recents/detail/<int:pk>/', SampleDetailView.as_view(), name='recents_detail'),
    path('recents/addcollection/<int:collection>', AddCollectionView.as_view(), name='recents_addcollection'),
    path('recents/addToUser', SampleAddToUser.as_view(), name='recents_sample_add_to_user'),
    path('switchTheme/', SwitchThemeView.as_view(), name='switch_theme'),
    path('profile/<int:pk>/', ProfileView.as_view(),name='profile'),
    path('updateProfileImage/<int:pk>/', UpdateProfileImage.as_view(), name='newProfileImage'),
    path('updateUserInfo/<int:pk>/', UpdateUserInfo.as_view(), name='changeUserInfo'),
    path('updateCollectionImage/<int:pk>/', UpdateCollectionImage.as_view(), name='newCollectionImage'),
    path('changePassword/<int:pk>', PasswordsChangeView.as_view(), name='changePassword'),
    path('switchMenu', SidebarView.as_view(), name="switchMenu"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('createKitFromSample/', CreateKitFromSample.as_view(), name='createKitFromSample'),
    path('createKitFromColl/', CreateKitFromColl.as_view(), name='createKitFromColl'),
    path('projects/', ProjectListView.as_view(), name='projectList'),
    path('projects/create', ProjectCreateView.as_view(), name='project_create'),

    #api
    path('api/collections/', CollectionAPIListView.as_view(), name='collection_list_api'),
    path('api/kit/<int:pk>/', GetKit.as_view(), name='getKit'),
    path('api/saveSubmenu/', SubMenuAPIView.as_view(), name='submenuAPI'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)