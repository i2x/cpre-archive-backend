from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class GetTokenByEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")  # Get email from frontend request

        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            # Get the user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email not found"}, status=404)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        })
