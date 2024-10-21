from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            name="testuser",
            email="testuser@gmail.com",
            password="testpassword",
            provider="EMAIL",
        )
        self.user.save()

    def test_update_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            "/auth/profile/", {"name": "newname",
                               "picture": "http://newpicture.com"}
        )
        self.assertEqual(response.status_code, 200)


class AuthEndpointsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            name="testuser",
            email="testuser@gmail.com",
            password="testpassword",
            provider="EMAIL",
        )
        self.user.save()

    def test_valid_login(self):
        response = self.client.post(
            "/auth/signin/", {"email": "testuser@gmail.com",
                              "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_password_login(self):
        response = self.client.post(
            "/auth/signin/",
            {"email": "testuser@gmail.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_email_login(self):
        response = self.client.post(
            "/auth/signin/",
            {"email": "doesntexist@gmail.com", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 400)

    def test_create_user(self):
        response = self.client.post(
            "/auth/signup/",
            {
                "name": "testuser2",
                "email": "testuser2@gmail.com",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_create_existing_user(self):
        response = self.client.post(
            "/auth/signup/",
            {
                "name": "testuser",
                "email": "testuser@gmail.com",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )
