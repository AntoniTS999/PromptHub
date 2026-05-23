from django.test import TestCase

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


