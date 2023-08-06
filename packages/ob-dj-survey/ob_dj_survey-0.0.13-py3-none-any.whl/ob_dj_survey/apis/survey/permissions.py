from rest_framework.permissions import BasePermission


class SurveyManagerPermission(BasePermission):
    """
    Allows access only to survey managers.
    Managers can create, update and list surveys, other users can view details
    """

    def has_permission(self, request, view):
        user = request.user
        view_manager = not (
            "pk" in request.parser_context["kwargs"] and request.method == "GET"
        )  # allow only retieve
        return not view_manager or (
            user
            and hasattr(user, "can_manage_surveys")
            and user.can_manage_surveys(request, view)
        )
