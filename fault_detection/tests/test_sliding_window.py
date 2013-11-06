from __future__ import with_statement
import unittest
from fault_detection.binomial_detector import BinomialDetector, Result
from fault_detection.sliding_window import SlidingWindowDetection, FailureDetectedException
from fault_detection.tests.results_builder import a_test_result_history


class TestSlidingWindow(unittest.TestCase):

    def setUp(self):
        self.sliding_window_detection = SlidingWindowDetection(self.a_detector(), window_size=20)


    def test_given_a_stream_of_results_uses_a_detector_to_detect_breakage(self):
        events = self.a_stream_of_results(size=1000).with_p_of_fail(1, since=500).build()
        try:

            self.sliding_window_detection.detect_failure(events)
            self.fail()
        except FailureDetectedException, exception:
            self.assertTrue(480 < exception.detected_at_element < 520)

    def a_detector(self):
        return BinomialDetector(10, 0.1, lambda x: x == Result.FAIL)

    def a_stream_of_results(self, size):
        return a_test_result_history().with_number_of_results(size)

    def test_does_nothing_if_frequency_didnt_increase(self):
        self.sliding_window_detection.detect_failure([
            Result.PASS,
            Result.PASS,
            Result.FAIL,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.FAIL,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
            Result.PASS,
        ])

    def test_raises_exception_if_frequency_increseas(self):
        regular_part_size = 80
        window_size = 20
        try:
            self.sliding_window_detection.detect_failure([Result.PASS, Result.FAIL]*(regular_part_size/2) + [
                Result.FAIL,
                Result.FAIL,
                Result.FAIL,
                Result.FAIL,
                Result.FAIL,
                Result.FAIL,
                Result.FAIL])
            self.fail("Expected exception FailureDetectedException")
        except FailureDetectedException, exception:
            self.assertTrue(exception.detected_at_element > (regular_part_size - window_size))
