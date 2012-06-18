import random
import unittest
import gmpy

def binomial(p, n, k):
    return gmpy.comb(n, k) * (pow(p, k)) * pow(1 - p, n - k)

def frequency_of_value(a_list, value):
    return sum(x == value and 1 or 0 for x in a_list)

class Detector(object):
    def __init__(self, history_size, threshold):
        self.history_size = history_size
        self.threshold = threshold

    def frequency_of_value(self, history, value):
        return sum(x == value and 1 or 0 for x in history)

    def detects_fail(self, test_results):
        test_results = test_results[:]
        if all(x == Result.PASS for x in test_results) or all(x == Result.FAIL for x in test_results):
            return False

        p_of_fail = float(frequency_of_value(test_results[:self.history_size], Result.FAIL)) / self.history_size
        detect_from = test_results[self.history_size:]
        number_of_fails_in_rest = frequency_of_value(detect_from, Result.FAIL)
        r = binomial(p=p_of_fail, n=len(detect_from), k=number_of_fails_in_rest)
        return r < self.threshold


class Result:
    PASS = "PASS"
    FAIL = "FAIL"


class TestResultHistoryBuilder(object):
    def __init__(self):
        self.number_of_results = 20
        self.p_ranges = []
        self.__with_noise = False

    def build(self):
        initial_set = [Result.PASS] * self.number_of_results
        for from_, to_, p, value_to_set in self.p_ranges:
            for i in range(from_, to_):
                if random.random() < p:
                    initial_set[i] = value_to_set

        if self.with_noise:
            initial_set = self.add_noise(initial_set)

        return initial_set

    def add_noise(self, test_results):
        test_results = test_results[:]
        for i in range(len(test_results)):
            if not (i % 3):
                test_results[i] = Result.FAIL
        return test_results

    def with_number_of_results(self, number_of_results):
        self.number_of_results = number_of_results
        return self

    def all_passing(self):
        self.p_ranges = []
        return self

    def with_p_of_fail(self, p, since):
        self.p_ranges.append((since, self.number_of_results, p, Result.FAIL))
        return self

    def with_all_fails(self):
        self.with_p_of_fail(1, 0)
        return self

    def with_noise(self):
        self.__with_noise = True
        return self


def a_test_result_history():
    return TestResultHistoryBuilder()


class TestDetector(unittest.TestCase):
    def setUp(self):
        self.detector = Detector(10, 0.1)

    def test_given_a_history_of_test_results_without_noise_where_the_test_began_to_fail_detects_fails(self):
        test_results = a_test_result_history().with_number_of_results(20).with_p_of_fail(1, since=10).build()
        self.assertTrue(self.detector.detects_fail(test_results))

    def test_given_a_history_of_test_results_with_all_fails_doesnt_detect_breakage(self):
        test_results = a_test_result_history().with_number_of_results(20).with_all_fails().build()
        self.assertFalse(self.detector.detects_fail(test_results))

    def test_given_a_history_of_test_results_without_noise_with_all_passing_doesnt_detect_approx_breakage_date(self):
        test_results = a_test_result_history().with_number_of_results(20).all_passing().build()
        self.assertFalse(self.detector.detects_fail(test_results))

    def test_given_a_history_of_test_results_with_noise_where_the_test_began_to_fail_constantly_detects_fails(self):
        test_results = a_test_result_history().with_number_of_results(20).with_p_of_fail(1, since=10).with_noise().build()
        self.assertTrue(self.detector.detects_fail(test_results))

    def test_given_a_history_of_test_results_with_noise_where_the_test_dont_began_to_fail_doesnt_detect_fails(self):
        test_results = a_test_result_history().with_number_of_results(20).with_noise().build()
        self.assertFalse(self.detector.detects_fail(test_results))
