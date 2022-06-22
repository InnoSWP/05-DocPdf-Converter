from rest_framework import generics, status
from rest_framework.response import Response


class IndexView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "converter": f'http://{request.META["HTTP_HOST"]}/convert',
            },
            status=status.HTTP_200_OK,
        )
