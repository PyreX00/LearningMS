from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.validators import ValidationError


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.groups.filter(name = "admin")

class StudentAccess(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            if (request.user.groups.filter(name = "Instructor") or request.user.groups.filter(name="Sponsor")):
                return True
        
        return request.user.groups.filter(name ="admin")

class StudentCourseAccess(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.groups.filter(name = "Instructor"):
            return True
        return request.user.groups.filter(name ='admin')
    
class StudentCourseProgressAccess(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.groups.filter(name = "Sponsor"):
            return True
        return request.user.groups.filter(name = 'admin') or request.user.groups.filter(name = 'Instructor')