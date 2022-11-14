from django.urls import path, include
from . import views
from . import url_handlers


urlpatterns = [
    path('pojistenci_index/', views.PojistenecIndex.as_view(), name='home'),
    path('create_pojistenec/', views.CreatePojistenec.as_view(),
         name='novy_pojistenec'),
    path('', url_handlers.index_handler),
    path('login/', views.UzivatelViewLogin.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.UzivatelViewRegister.as_view(), name='registrace'),
    path('edit/<str:pk>/', views.EditPojistenec.as_view(), name='edit_pojistenec'),
    path('pojistenec_detail/<str:pk>/',
         views.AktualPojistenec.as_view(), name='pojistenec_detail'),
    path('create_pojisteni/<str:pk>', views.CreatePojisteni.as_view(), name='create_pojisteni'),
    path('update_pojisteni/<str:pk>', views.UpdatePojisteni.as_view(), name='update_pojisteni'),
    path('delete_pojisteni/<str:pk>', views.delete_pojisteni, name='delete_pojisteni'),
]
