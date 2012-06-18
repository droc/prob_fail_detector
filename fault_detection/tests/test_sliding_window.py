import unittest
from fault_detection.binomial_detector import BinomialDetector
from fault_detection.tests.results_builder import a_test_result_history

class SlidingWindowDetection(object):
    def __init__(self, a_detector, window_size):
        self.a_detector = a_detector
        self.window_size = window_size

    def detect_failure(self, events):
        i = 0
        while (i + self.window_size) < len(events):
            if self.a_detector.detects_fail(events[i : i + self.window_size]):
                raise FailureDetectedException(i)
            i += 1

class FailureDetectedException(Exception):
    def __init__(self, detected_at_element, *args, **kw):
        super(FailureDetectedException, self).__init__(*args, **kw)
        self.detected_at_element = detected_at_element


class TestSlidingWindow(unittest.TestCase):
    def test_given_a_stream_of_results_uses_a_detector_to_detect_breakage(self):
        sw = SlidingWindowDetection(self.a_detector(), window_size=20)
        events = self.a_stream_of_results(size=1000).with_p_of_fail(1, since=500).build()
        with self.assertRaises(FailureDetectedException) as failure_exception:
            sw.detect_failure(events)
        self.assertTrue(480 < failure_exception.exception.detected_at_element < 520)

# [p, f, f, f, f, f, f]
# [f, p, f, p, f, p, f, p]

    def a_detector(self):
        return BinomialDetector(10, 0.1)

    def a_stream_of_results(self, size):
        return a_test_result_history().with_number_of_results(size)