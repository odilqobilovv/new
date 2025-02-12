from rest_framework.permissions import BasePermission

class IsUsingRegisteredDevice(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        device_id = request.headers.get("Device-ID")

        if not user.first_registered_device:
            user.first_registered_device = device_id
            user.save()
            return True

        return user.first_registered_device == device_id