import numpy as np
import scipy.stats as stats
from enum import Enum, EnumMeta, unique


class Analysis:
    def remove_outliers_iqr(data):
        data = np.array(data)
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        mask = (data >= lower_bound) & (data <= upper_bound)
        return data[mask]

    def calculate_chi_square(data):
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

    def calculate_max_entropy(data):
        # Maybe log2(n^l), n = size, l = bits in each point
        return np.log2(len(data))

    def calculate_most_common_value(data):
        values, counts = np.unique(data, return_counts=True)
        probabilities = counts / counts.sum()
        most_common_prob = np.max(probabilities)

        upper_bound = most_common_prob + 2.576 * np.sqrt(
            (most_common_prob * (1 - most_common_prob))
            / (len(data) - 1)
        )

        most_common_value = min(1, upper_bound)
        min_entropy_estimate = -np.log2(most_common_value)

        return min_entropy_estimate


class MetricTypeMeta(EnumMeta):
    def __getitem__(self, metric_name: str):
        for member in self:
            if member.metric_name == metric_name:
                return member
        raise KeyError(f"MetricType with name '{metric_name}' not found.")


@unique
class MetricType(Enum, metaclass=MetricTypeMeta):
    Min_Entropy = (
        'Min Entropy',
        Analysis.calculate_min_entropy
    )
    MostCommonValue = (
        'Most Common Value',
        Analysis.calculate_most_common_value
    )
    Shannon_Entropy = (
        'Shannon Entropy',
        Analysis.calculate_shannon_entropy
    )
    Chi_Square = (
        'Chi Square',
        Analysis.calculate_chi_square
    )
    MaxEntropy = (
        'Max Entropy',
        Analysis.calculate_max_entropy
    )

    def __init__(self, metric_name: str, func):
        self.metric_name = metric_name
        self.func = func
