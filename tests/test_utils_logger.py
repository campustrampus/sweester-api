"""
Test for utils.logger
"""
import unittest
from sweester.utils.logger import raise_ni


class LoggerTests(unittest.TestCase):
    """
    LoggerTests includes all unit tests for reaper.urils.logger module
    """
    def setUp(self):
        """setup for test"""
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_get_logger(self):
        from sweester.utils.logger import get_logger
        logger = get_logger(__name__)
        self.assertEqual(logger.name, 'tests.test_utils_logger')
        logger.debug('logger name: %s', logger.name)
        logger.warn('logger warning ...')

    def test_raise_ni(self):
        """
        test reaper.utils.logger.raise_ni
        """
        method_name = 'some_method_name'
        msg = 'must implement {} in derived class'.format(method_name)
        with self.assertRaises(NotImplementedError) as context:
            result = raise_ni(method_name)
            self.assertIsNone(result)
            self.assertEqual(msg, context.exception.message)
