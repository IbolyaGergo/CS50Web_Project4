from django.test import TestCase
from .models import User, Post

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):

        # Create users
        user1 = User.objects.create_user(username="user1", email="user1@user1.com", password="user1")
        user2 = User.objects.create_user(username="user2", email="user2@user2.com", password="user2")
        user3 = User.objects.create_user(username="user3", email="user3@user3.com", password="user3")

    def test_following_count(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        user3 = User.objects.get(username="user3")

        user1.following.add(user2)
        user1.following.add(user3)

        self.assertEqual(user1.following.count(), 2)
        user3.delete()
        self.assertEqual(user1.following.count(), 1)


    def test_followers_count(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        user3 = User.objects.get(username="user3")

        user1.following.add(user2)
        user3.following.add(user2)

        self.assertEqual(user2.followers.count(), 2)
        user3.delete()
        self.assertEqual(user2.followers.count(), 1)
    
