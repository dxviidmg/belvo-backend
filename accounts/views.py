from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Profile

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.is_staff == True or user.is_superuser == True:
            belvo_link = None
        else:
            profile = Profile.objects.get(user=user)
            belvo_link = profile.belvo_link
        return Response({
            'token': token.key,
            'belvo_link': belvo_link,
        })