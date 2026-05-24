from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from prompts.models import Category, Prompt

CATEGORY_CREATE_URL = reverse("prompts:category-create")
CATEGORY_LIST_URL = reverse("prompts:category-list")


class PublicCategoryTest(TestCase):

    def test_login_required(self):
        """
        test that only authenticated users can create categories
        :return:
        """
        response = self.client.get(CATEGORY_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCategoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="123test"
        )
        self.client.force_login(self.user)

    def test_retrieve_categories(self):
        """
        Test that authenticated user can retrieve list of categories
        :return:
        """
        Category.objects.create(name="test")
        Category.objects.create(name="test2")
        response = self.client.get(CATEGORY_LIST_URL)
        categories = Category.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]), list(categories)
        )
        self.assertTemplateUsed(response, "prompts/category_list.html")

    def test_update_data_prompt(self):
        """
        test that update prompt data is correct(title, categories)
        :return:
        """
        category = Category.objects.create(name="test")
        category2 = Category.objects.create(name="test2")
        self.prompt = Prompt.objects.create(
            title="Ann",
            author=self.user,
            content="test content" * 20,
        )
        self.prompt.categories.add(category,category2)
        url = reverse("prompts:prompt-update", args=[self.prompt.id])
        new_category = Category.objects.create(name="New Category")
        response = self.client.post(
            url,
            {
                "title": "New Title",
                "categories": [new_category.id],
                "author": self.user.id,
                "content": "test content" * 20,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.prompt.refresh_from_db()
        self.assertEqual(self.prompt.categories.count(), 1)
        self.assertEqual(self.prompt.title, "New Title")

