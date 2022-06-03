from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class HasOriginalImage(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.plan.original_image


class HasPlan(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.plan
