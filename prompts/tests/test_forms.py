from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from prompts.forms import AuthorCreationForm


class FormsTest(TestCase):
    def test_form_with_first_name_last_name_email_display_name_valid(self):
        """
        Test that the form is valid and displayed data correctly.
        :return:
        """
        form_data = {
            "username": "userAdam",
            "first_name": "Adam",
            "last_name": "Smith",
            "email": "adam@gmail.com",
            "display_name": "AdaS",
            "password1": "user123test",
            "password2": "user123test",
        }
        form = AuthorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

class AuthorCreationTest(TestCase):

    def test_create_author(self):
        """
        test checking if author creating correctly from form_data and redirect to success url after creation
        :return:
        """
        form_data = {
            "username": "userPawel",
            "first_name": "Pawel",
            "last_name": "Black",
            "email": "paw_black@gmail.com",
            "display_name": "PawelB",
            "password1": "123test123",
            "password2": "123test123",
        }
        response = self.client.post(reverse("prompts:author-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.email, form_data["email"])
        self.assertEqual(new_user.display_name, form_data["display_name"])
