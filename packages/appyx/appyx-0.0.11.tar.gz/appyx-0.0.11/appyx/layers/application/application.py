from appyx.layers.application.exception_handler import AddExceptionToResult


class Application:
    """
    Models an application.
    Given a running environment it creates the resources that will be used by the business.
    It also defines and set up the interfaces with which external actors will interact with the business.

    An application also defines how to handle the exceptions those might rise for the resources the business uses.
    """

    @classmethod
    def running_environment_test_dev(cls):
        return 'TEST_DEV'

    def __init__(self, running_environment=None, exception_handler=None) -> None:
        super().__init__()
        self._business = None
        self._general_exception_handler = exception_handler or self._default_exception_handler()
        if running_environment is None:
            running_environment = self.running_environment_test_dev()
        self._running_environment = running_environment

    def general_exception_handler(self):
        return self._general_exception_handler

    def set_general_exception_handler(self, exception_handler):
        self._general_exception_handler = exception_handler

    def _default_exception_handler(self):
        return AddExceptionToResult()

    def current_business(self):
        if self._business is None:
            self._business = self._new_business()
        return self._business

    def _new_business(self):
        from polls.domain.poll_station import PollStation, FakeClock, QuestionsArchive
        business = None
        if self._running_environment == self.running_environment_test_dev():
            clock = FakeClock()
            business = PollStation(clock, QuestionsArchive())
        return business
