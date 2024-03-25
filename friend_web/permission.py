from rest_framework import permissions
from .models import Connection, CustomUser
from django.db.models import Q
import uuid

class MaxAccessPermission(permissions.BasePermission):
    """
    Takes current_user_id
    create sets of allowed user id
    create sets of allowed connections
    add set data with loop O(N ^ max depth) optimizable
    returns if request data in loop
    Args:
        current_user_id
    Returns:
        Boolean
    """
    message = 'You have reached out of your authorization'

    def has_permission(self, request, view):
        MAX_BREADTH = 4
        current_user_id = request.user.id
        allowed_userdata_id = set([current_user_id])
        allowed_connection_id = set()

        # Extracting data from request
        request_data_id = request.data.get("user_id")
        request_connection_id = request.data.get("connection_id")

        for i in range(MAX_BREADTH - 1):
            for user in allowed_userdata_id.copy():
                connection_list = Connection.objects.filter(Q(inviter=user) | Q(invitee=user)).values()
                if connection_list:
                    for row in connection_list:
                        # Adding related users and connections
                        allowed_userdata_id.add(row["inviter_id"])
                        allowed_userdata_id.add(row["invitee_id"])
                        allowed_connection_id.add(row["id"])

        # Check if request_data_id and request_connection_id are present
        if request_data_id and request_connection_id:
            return False
        elif request_data_id:
            # Convert request_data_id to UUID object for comparison
            request_data_id = uuid.UUID(request_data_id)
            return request_data_id in allowed_userdata_id
        elif request_connection_id:
            # Convert request_connection_id to UUID object for comparison
            request_connection_id = uuid.UUID(request_connection_id)
            return request_connection_id in allowed_connection_id

        return True  # Return True by default if no condition matches

class EmailVeridiedPermission(permissions.BasePermission):
    """
        Takes curren_user_id
        Takes requested connection id
        returns if request data in loop
    Args:
        current_user_id
    Returns:
        Boolean
    """
    message = 'You are not verified!'
    def has_permission(self, request, view):
        current_user = request.user
        return current_user.email_is_verified

class SelfConnectionPermission(permissions.BasePermission):
    """
        Takes curren_user_id
        Takes requested connection id
        returns if request data in loop
    Args:
        current_user_id
    Returns:
        Boolean
    """
    message = 'You can\'t edit connection that is not yours'
    def has_permission(self, request, view):
        current_user_id = request.user.id
        request_connection_id = request.data.get("connection_id")
        connection_list = Connection.objects.filter(Q(inviter=current_user_id) | Q(invitee=current_user_id))

        # Check if request_connection_id exists in connection_list
        if connection_list.filter(id=request_connection_id).exists():
            return True

        # If request_connection_id does not exist in connection_list
        return False
