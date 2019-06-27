from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the onwer of this listing to execute this action." #403 forbidden
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user #author: Product instance.author