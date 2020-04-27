from django.urls import include, path

# API URLS
urlpatterns = [
    # API base url
    path("users/", include("api.users.urls")),
    path("auth/", include("api.auths.urls")),
    path("", include("api.ecommerces.urls"))
]
urlpatterns = [path("api/v1/", include(urlpatterns))]
