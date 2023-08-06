from appyx.layers.application.application import Application


class Environment:
    CURRENT_APP = None

    def current_app(self):
        if self.__class__.CURRENT_APP is None:
            self.__class__.CURRENT_APP = self._new_application()
        return self.__class__.CURRENT_APP

    def _new_application(self):
        running_environment = Application.running_environment_test_dev()
        return Application(running_environment)
