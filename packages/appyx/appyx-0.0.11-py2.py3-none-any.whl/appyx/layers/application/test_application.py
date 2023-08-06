from unittest import TestCase

from appyx.layers.application.environment import Environment


class ApplicationTest(TestCase):

    def test_01_answers_the_same_business(self):
        first_asked_business = Environment().current_app().current_business()

        second_asked_business = Environment().current_app().current_business()

        self.assertIs(first_asked_business, second_asked_business)
