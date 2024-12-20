from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS



class MyIsAuthenticatedOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user == obj.user
        return super().has_object_permission(request, view, obj)