import numpy as np
class Statistics:
    def chi_square(data):
        # Bin the jitter values into frequency counts
        num_bins = len(set(data)) # Unique jitter values determine bins
        observed_freq, bin_edges = np.histogram(data, bins=num_bins)

        # Expected frequencies assuming uniform distribution
        expected_freq = np.full_like(observed_freq, np.mean(observed_freq))

        # Manually compute Chi-Square Statistic
        chi2_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)

        # Display results
        print(f'Observed Frequencies: {observed_freq}')
        print(f'Expected Frequencies: {expected_freq}')
        print(f'\nChi-Square Statistic: {chi2_stat:.4f}')

        # Interpretation (without p-value since SciPy is unavailable)
        alpha = 0.05 # 5% significance level
        critical_value = 16.92 # Approx. chi-square critical value for df=8, alpha=0.05

        if chi2_stat > critical_value:
            print('\nReject the null hypothesis: Jitter is NOT uniformly distributed.')
        else:
            print('\nFail to reject the null hypothesis: Jitter follows a uniform distribution.')

        return chi2_stat

    def calculate_shannon_entropy(data):
        '''Calculate Shannon entropy of a dataset.'''
        values, counts = np.unique(data, return_counts=True)
        probabilities = counts / counts.sum()
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    def calculate_min_entropy(data):
        values, counts = np.unique(data, return_counts=True)
        probabilities = counts / counts.sum()

        min_entropy = -np.log2(np.max(probabilities))

        return min_entropy

    statistics_map = {
            'Min-Entropy': calculate_min_entropy,
            'Shannon Entropy': calculate_shannon_entropy,
            'Chi Square': chi_square,
    }

    # # Example Usage
    # data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]  # Replace with your actual dataset
    # entropy_value = shannon_entropy(data)
    # print(f'Shannon Entropy: {entropy_value:.4f}')
