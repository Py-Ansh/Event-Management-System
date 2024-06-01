"""
URL configuration for Event_Management_Sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Events.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),

    path("login", login_usr, name="loginpage"),
    path("signup", signup, name="signup"),
    path("logout", logout_usr, name="logout"),

    path("dummypayment", dummypayment),
    path("pay_n_participate", pay_n_participate),

    path("myevents", myevents, name="myevents"),

    path("create_event", create_event, name="create_event"),
    path("editevent", get_editevent_details),
    path("fill_edit_details", fill_edit_details),

    path("cancel_participation", manage_cancellation),
    path("refund", cancel_participation),

    path("search", search),

    path("complete_event", mark_as_completed),

    path("participants", participants)
]
