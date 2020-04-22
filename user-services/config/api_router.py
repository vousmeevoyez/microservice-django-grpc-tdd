from api.users.urls import urlpatterns as \
    users_url_patterns
from api.auths.urls import urlpatterns as \
    auth_url_patterns

urlpatterns = []
urlpatterns += users_url_patterns
urlpatterns += auth_url_patterns
