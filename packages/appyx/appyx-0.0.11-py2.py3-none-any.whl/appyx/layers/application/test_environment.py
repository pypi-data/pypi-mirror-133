from unittest import TestCase

from appyx.layers.application.environment import Environment


class EnvironmentTest(TestCase):

    def test_01_answers_the_same_application(self):
        first_asked_app = Environment().current_app()

        second_asked_app = Environment().current_app()

        self.assertIs(first_asked_app, second_asked_app)
