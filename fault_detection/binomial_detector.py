import gmpy

def binomial(p, n, k):
    return gmpy.comb(n, k) * (pow(p, k)) * pow(1 - p, n - k)

def frequency_of_value(a_list, a_test):
    return sum(a_test(x) and 1 or 0 for x in a_list)

class BinomialDetector(object):
    def __init__(self, history_size, threshold, a_test):
        self.history_size = history_size
        self.threshold = threshold
        self.a_test = a_test

    def detects_fail(self, test_results):
        if frequency_of_value(test_results, self.a_test) in (0, len(test_results)):
            return False
        test_results = test_results[:]

        p_of_fail = float(frequency_of_value(test_results[:self.history_size], self.a_test)) / self.history_size
        detect_from = test_results[self.history_size:]
        number_of_fails_in_rest = frequency_of_value(detect_from, self.a_test)
        r = binomial(p=p_of_fail, n=len(detect_from), k=number_of_fails_in_rest)
        return r < self.threshold


class Result:
    PASS = "PASS"
    FAIL = "FAIL"
