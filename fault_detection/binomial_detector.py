import gmpy

def binomial(p, n, k):
    return gmpy.comb(n, k) * (pow(p, k)) * pow(1 - p, n - k)

def frequency_of_value(a_list, value):
    return sum(x == value and 1 or 0 for x in a_list)

class BinomialDetector(object):
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
