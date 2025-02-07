import requests
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# ✅ Helper Function to Generate Tokens
def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# ✅ Google
def get_user_from_google_token(token):
    google_url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
    response = requests.get(google_url)

    if response.status_code != 200:
        return None

    return response.json()




class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        data = get_user_from_google_token(token)

        if not data:
            return Response({'error': 'Invalid Google token'}, status=400)

        email = data.get('email')  # ✅ Get the real email
        name = data.get('name')  # ✅ Get the user's name
        picture = data.get('picture')  # ✅ Get the profile picture URL

        if not email:
            return Response({'error': 'Email not found in Google response'}, status=400)

        # Ensure username is unique and meaningful
        username = email.split('@')[0]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': username}  # Use the part before '@' for username
        )

        if created:
            user.role = 'member'
            user.save()

        tokens = generate_tokens_for_user(user)

        return Response({
            'refresh': tokens["refresh"],
            'access': tokens["access"],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,  # ✅ Return the real email
                'role': user.role,
                'picture': picture  # ✅ Return the Google profile picture
            }
        })
