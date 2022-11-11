from django.urls import path, include
from . import views
from . import url_handlers


urlpatterns = [
    path('pojistenci_index/', views.PojistenecIndex.as_view(), name='pojistenci'),
    path('create_pojistenec/', views.CreatePojistenec.as_view(),
         name='novy_pojistenec'),
    path('', url_handlers.index_handler),
    path('login/', views.UzivatelViewLogin.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.UzivatelViewRegister.as_view(), name='registrace'),
    path('<str:pk>/edit/', views.EditPojistenec.as_view(), name='edit_pojistenec'),
    path('<str:pk>/pojistenec_detail/',
         views.AktualPojistenec.as_view(), name='pojistenec_detail'),

]
