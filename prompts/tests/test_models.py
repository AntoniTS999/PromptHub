from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from prompts.models import Category, Prompt, Rating


class ModelsTest(TestCase):

    def test_category_str(self):
        """
        test if category string is correct (should show category.display_name)
        :return:
        """
        category = Category(name="test")
        self.assertEqual(str(category), "test")

    def test_author_with_display_name_str(self):
        """
        - test if author with display name string is correct
        (should show author.display_name)
        - test if author password is correctly
        hashed and verifiable
        :return:
        """
        username = "test"
        password = "123test"
        display_name = "name_on_the_screen"
        author = get_user_model().objects.create_user(
            username=username,
            password=password,
            display_name=display_name,
        )
        self.assertEqual(str(author), author.display_name)
        self.assertTrue(author.check_password(password))

    def test_author_without_display_name_str(self):
        username = "test"
        password = "123test"
        author = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.assertEqual(str(author), author.username)

    def test_prompt_str(self):
        """
        test if prompt string is correct:
        especially preview for content with
        25 symbols and format of creation/update
        datetime
        :return:
        """
        author = get_user_model().objects.create_user(
            username="test",
            password="123test",
        )
        prompt = Prompt(
            author=author,
            title="testTitle",
            content="lorem50" * 50,
            created_at=datetime(2025, 5, 21, 15, 33, 00),
            updated_at=datetime(2026, 5, 22, 14, 38, 25),
        )
        self.assertEqual(
            str(prompt),
            f"{prompt.title} "
            f"| {prompt.author} "
            f"| 05/21/2025 15:33:00 "
            f"| 05/22/2026 14:38:25 "
            f"| {prompt.content[:25]}",
        )

    def test_rating_str(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="123test",
        )
        prompt = Prompt(
            author=user,
            title="testTitle",
            content="lorem50" * 50,
            created_at=datetime(2025, 5, 21, 15, 33, 00),
            updated_at=datetime(2026, 5, 22, 14, 38, 25),
        )
        rating = Rating(
            prompt=prompt,
            user=user,
            value=5,
        )
        self.assertEqual(str(rating), str(rating.value))
