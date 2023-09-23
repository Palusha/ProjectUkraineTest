from django.http import Http404
from rest_framework import generics

from .models import UserBar
from .permissions import IsOwnerOrReadOnly
from .serializers import UserBarSerializer


class UserBarRetriveUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserBar.objects.all()
    serializer_class = UserBarSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "product_id"

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise Http404

        obj, _ = UserBar.objects.get_or_create(
            user=self.request.user,
            product_id=self.kwargs.get("product_id"),
        )
        return obj
