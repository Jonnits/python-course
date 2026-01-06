from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            name="Test User",
            email_address="test@example.com"
        )
    
    def test_userprofile_name(self):
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.name, "Test User")
    
    def test_userprofile_str(self):
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), "Test User")