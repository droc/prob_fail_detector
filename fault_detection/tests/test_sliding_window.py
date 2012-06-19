from __future__ import with_statement
import unittest
from test_case_reports.status import Status
from fault_detection.binomial_detector import BinomialDetector
from fault_detection.sliding_window import SlidingWindowDetection, FailureDetectedException
from fault_detection.tests.results_builder import a_test_result_history


class TestSlidingWindow(unittest.TestCase):
    def test_given_a_stream_of_results_uses_a_detector_to_detect_breakage(self):
        sw = SlidingWindowDetection(self.a_detector(), window_size=20)
        events = self.a_stream_of_results(size=1000).with_p_of_fail(1, since=500).build()
        try:

            sw.detect_failure(events)
            self.fail()
        except FailureDetectedException, exception:
            self.assertTrue(480 < exception.detected_at_element < 520)

    def a_detector(self):
        return BinomialDetector(10, 0.1, lambda x: x == Status.FAIL)

    def a_stream_of_results(self, size):
        return a_test_result_history().with_number_of_results(size)