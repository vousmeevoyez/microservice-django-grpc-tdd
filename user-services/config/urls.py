from django.urls import include, path

# API URLS
urlpatterns = [
    # API base url
    path("users/", include("api.users.urls")),
]
