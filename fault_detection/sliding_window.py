from exceptions import Exception

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