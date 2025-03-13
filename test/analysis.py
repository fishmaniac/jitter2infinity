import numpy as np
import scipy.stats as stats
from enum import Enum, EnumMeta, unique


class Analysis:
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

        alpha = 0.05 # 5% significance level
        critical_value = stats.chi2.ppf(1.0 - alpha, num_bins - 1)

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
        print("Shannon entropy: ", entropy)

        return entropy

    def calculate_min_entropy(data):
        values, counts = np.unique(data, return_counts=True)
        probabilities = counts / counts.sum()

        min_entropy = -np.log2(np.max(probabilities))
        print("Min entropy: ", min_entropy)

        return min_entropy


class MetricTypeMeta(EnumMeta):
    def __getitem__(self, metric_name: str):
        for member in self:
            if member.metric_name == metric_name:
                return member
        raise KeyError(f"MetricType with name '{metric_name}' not found.")


@unique
class MetricType(Enum, metaclass=MetricTypeMeta):
    Min_Entropy = ('Min Entropy', Analysis.calculate_min_entropy)
    Shannon_Entropy = ('Shannon Entropy', Analysis.calculate_shannon_entropy)
    Chi_Square = ('Chi Square', Analysis.chi_square)

    def __init__(self, metric_name: str, func):
        self.metric_name = metric_name
        self.func = func
