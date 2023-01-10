from django.urls import path
from .views import *

app_name = "everestapp"

urlpatterns = [
    path("", ClientHomeView.as_view(), name="clienthome"),
    path("service/", ClientServiceView.as_view(), name="clientservice"),
    path("about/", ClientAboutView.as_view(), name="clientabout"),
    path("contact/", ClientContactView.as_view(), name="clientcontact"),
    path("news/", ClientNewsListView.as_view(), name="clientnewslist"),
    path("news/<int:pk>/", ClientNewsDetailView.as_view(), name="clientnewsdetail"),
    path('newscommentcreate/<int:pk>/', ClientNewsCommentCreateView.as_view(),      name='clientnewscommentcreate'),
    path("news/create/",
        ClientNewsCreateView.as_view(), name="clientnewscreate"),
    path("news/update/<int:pk>/",
        ClientNewsUpdateView.as_view(), name="clientnewsupdate"),
    path("news/delete/<int:pk>/",
        ClientNewsDeleteView.as_view(), name="clientnewsdelete"),  
    path("admin/login/",
        AdminLoginView.as_view(), name="adminlogin"),
    path("admin/logout/",
        AdminLogoutView.as_view(), name="adminlogout"),  
]