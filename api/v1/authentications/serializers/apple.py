import base64
import json

import jwt
import requests
from rest_framework import serializers
from jwt.exceptions import JWTDecodeError
from rest_framework.exceptions import ValidationError

from api.v1.accounts.serializers import ProfileSerializer


class AppleSignInSerializer(serializers.Serializer):
    APPLE_PUBLIC_KEY_URL = 'https://appleid.apple.com/auth/keys'

    token = serializers.CharField(write_only=True)

    @staticmethod
    def get_unverified_header(token):
        header_segment = token.split('.')[0]
        # Add the required padding
        padding = '=' * (4 - (len(header_segment) % 4))
        header_data = base64.urlsafe_b64decode(header_segment + padding)
        return json.loads(header_data.decode('utf-8'))

    def validate(self, attrs):
        token = attrs['token']
        try:
            headers = {'kid': self.get_unverified_header(token)['kid']}
            apple_public_key = requests.get(self.APPLE_PUBLIC_KEY_URL, headers=headers).json()
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(apple_public_key)
            decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], audience='YOUR_APP_ID')
            # Generate and return an access token for your app (e.g., JWT)
        except JWTDecodeError:
            raise ValidationError({'token': 'Invalid token.'})

        print(decoded_token)
        # user_id = decoded_token['sub']
        # email = decoded_token['email']
        # user = CustomUser.objects.get_or_create(apple_id=user_id, email=email)
        return attrs
