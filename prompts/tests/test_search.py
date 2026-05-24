from datetime import datetime
from django.test import TestCase
from django.urls import reverse

from prompts.models import Category, Author, Prompt


class SearchTest(TestCase):
    def setUp(self):

        self.author = Author.objects.create_user(
            username="username_author",
            password="123test123",
            display_name="NameDisplay",
        )
        self.category = Category.objects.create(name="Test Category")
        self.prompt = Prompt.objects.create(
            author=self.author,
            title="Check_Title",
            content="Test Content",
            created_at=datetime(2025, 5, 21, 15, 33, 00),
            updated_at=datetime(2026, 5, 22, 14, 38, 25),
        )
        self.prompt.categories.add(self.category)
        self.client.force_login(self.author)

    def test_search_category(self):
        """
        Test that the search category by name works correctly.
        :return:
        """
        response = self.client.get(reverse("prompts:category-list")
                                   + "?name=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_search_prompt(self):
        """
        Test that the search prompt by title works correctly.
        :return:
        """
        response = self.client.get(reverse("prompts:prompt-list")
                                   + "?title=Title")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.prompt.title)

    def test_search_author(self):
        """
        Test that the search author by display_name works correctly.
        :return:
        """
        response = self.client.get(
            reverse("prompts:author-list") + "?display_name=Display"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.display_name)

    def test_search_author_by_username_when_display_name_not_exists(self):
        self.author_2 = Author.objects.create(
            username="username_author_2",
            password="123test",
        )
        response = self.client.get(reverse("prompts:author-list")
                                   + "?username=user")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author_2.username)

    def test_search_no_result(self):
        """
        Test that no result for display_name works correctly on search.
        :return:
        """
        response = self.client.get(
            reverse("prompts:author-list") + "?display_name=Piotr"
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["author_list"], [])
