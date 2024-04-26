from rest_framework.permissions import BasePermission, SAFE_METHODS
class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["post"]:
            return bool(request.user and request.user.is_authenticated)

        if view.basename in ["post-comment"]:
            if request.method in ["DELETE"]:
                return bool(
                    # como se va a eliminar, permito que el superusuario o el autor del post o el autor del comentario elimine
                    request.user.is_superuser
                    or request.user in [obj.author, obj.post.author]
                )

            return bool(request.user and request.user.is_authenticated)
        
        return False

    # verifico si el usuario tiene permisos para acceder a esta vista
    def has_permission(self, request, view):
        if view.basename in ["post","post-comment"]:  # si el viewset es de post
            # si el usuario es anonimo, solo permito los metodos seguros (GET, HEAD, OPTIONS)
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS
            return bool(
                request.user  # solo permito que el usuario autenticado pueda acceder a esta vista
                and request.user.is_authenticated
            )
        return False