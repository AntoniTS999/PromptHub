from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="123test",
        )
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_user(
            username="author",
            password="admin123test",
            display_name="author_test",
        )

    def test_author_display_name_listed(self):
        """
        test that the author display_name listed in admin panel
        :return:
        """
        url = reverse("admin:prompts_author_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.author.display_name)

    def test_author_display_name_listed_on_detail(self):
        """
        test that the author display_name listed on details at admin page
        :return:
        """
        url = reverse("admin:prompts_author_change", args=(self.author.id,))
        response = self.client.get(url)
        self.assertContains(response, self.author.display_name)
