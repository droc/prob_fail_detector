import random
from fault_detection.binomial_detector import Result

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