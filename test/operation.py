from ffi import FFI
import numpy as np

class Operation:
    def __init__(self, ffi: FFI, name="Unknown"):
        self.ffi = ffi
        self.name = name

    def run(self, lib_counter_func: FFI, iterations=100):
        time_diffs = []
        for i in range(0, iterations):
            diff = lib_counter_func(self.ffi)
            time_diffs.append(diff)
        return time_diffs, self.name

class Statistics:
    def chi_square(data):
        # Simulated jitter data (time variations in milliseconds)
        jitter_values = np.random.randint(1, 10, 100) # Replace with real jitter data if available

        # Bin the jitter values into frequency counts
        num_bins = len(set(jitter_values)) # Unique jitter values determine bins
        observed_freq, bin_edges = np.histogram(jitter_values, bins=num_bins)

        # Expected frequencies assuming uniform distribution
        expected_freq = np.full_like(observed_freq, np.mean(observed_freq))

        # Manually compute Chi-Square Statistic
        chi2_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)

        # Display results
        print(f"Observed Frequencies: {observed_freq}")
        print(f"Expected Frequencies: {expected_freq}")
        print(f"\nChi-Square Statistic: {chi2_stat:.4f}")

        # Interpretation (without p-value since SciPy is unavailable)
        alpha = 0.05 # 5% significance level
        critical_value = 16.92 # Approx. chi-square critical value for df=8, alpha=0.05

        if chi2_stat > critical_value:
            print("\nReject the null hypothesis: Jitter is NOT uniformly distributed.")
        else:
            print("\nFail to reject the null hypothesis: Jitter follows a uniform distribution.")
    def shannon_entropy(data):
        """Calculate Shannon entropy of a dataset."""
        values, counts = np.unique(data, return_counts=True)
        probabilities = counts / counts.sum()
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    # # Example Usage
    # data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]  # Replace with your actual dataset
    # entropy_value = shannon_entropy(data)
    # print(f"Shannon Entropy: {entropy_value:.4f}")
