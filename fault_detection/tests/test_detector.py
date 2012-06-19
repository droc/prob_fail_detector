import unittest
from fault_detection.binomial_detector import  BinomialDetector
from test_case_reports.status import Status
from fault_detection.tests.results_builder import  a_test_result_history


class TestDetector(unittest.TestCase):
    def setUp(self):
        self.detector = BinomialDetector(10, 0.1, lambda x: x == Status.FAIL)

    def test_given_a_history_of_test_results_without_noise_where_the_test_began_to_fail_detects_fails(self):
        test_results = self.results().with_p_of_fail(1, since=10).build()
        self.assertTrue(self.detector.detects_fail(test_results))

    def test_given_a_history_of_test_results_with_all_fails_doesnt_detect_breakage(self):
        test_results = self.results().with_all_fails().build()
        self.assertFalse(self.detector.detects_fail(test_results))

    def test_given_a_history_of_test_results_without_noise_with_all_passing_doesnt_detect_approx_breakage_date(self):
        test_results = self.results().all_passing().build()
        self.assertFalse(self.detector.detects_fail(test_results))

    def results(self):
        return a_test_result_history().with_number_of_results(20)

    def test_given_a_history_of_test_results_with_noise_where_the_test_began_to_fail_constantly_detects_fails(self):
        test_results = self.results().with_p_of_fail(1, since=10).with_noise().build()
        self.assertTrue(self.detector.detects_fail(test_results))

    def test_given_a_history_of_test_results_with_noise_where_the_test_dont_began_to_fail_doesnt_detect_fails(self):
        test_results = self.results().with_noise().build()
        self.assertFalse(self.detector.detects_fail(test_results))
