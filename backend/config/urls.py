"""
Companion OS — URL configuration.
Every request enters here. Routes are added as apps are built.
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


# Temporary home view — placeholder until the real chat interface is built
def home(request):
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect("accounts:login")
    return HttpResponse(f"Logged in as {request.user.username}. Home coming soon.")


urlpatterns = [
    # Django admin — for you to manage the app from a browser
    path("admin/", admin.site.urls),

    path("", home, name="home"),

    # Accounts — login, logout, register
    path("accounts/", include("apps.accounts.urls")),

    # App routes — uncomment as each app is built
    # path("chat/", include("apps.chat.urls")),
]
