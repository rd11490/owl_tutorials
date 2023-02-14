from scipy import stats
import numpy as np

original_distribution = [0, 1, 3, 3, 5, 5, 5, 5, 7, 7, 9, 10]

avg_orig = np.mean(original_distribution)
stdev_orig = np.std(original_distribution)

print(f'The Original Distribution is {original_distribution}')
print(f'It has a mean of {avg_orig} and stdev of {round(stdev_orig, 2)}')

for i in range(0, 11):
    z = (i - avg_orig) / stdev_orig
    percentile = stats.norm.cdf(z)
    print(f'A Value of {i} as a Z-score of {round(z,2)} and is in the {round(100 * percentile, 2)} Percentile of values')

print('Lets now double our population with new values with the majority being on the left side of the distrubtion')
new_values = [0, 1, 1, 2, 2, 3, 3, 4, 5, 8]
print(f'We will add the following values to our distribution {new_values}')
new_distribution = sorted(original_distribution + new_values)
print(f'Our new distribution is {new_distribution}')
avg_new = np.mean(new_distribution)
stdev_new = np.std(new_distribution)
print(f'The new distribution has a mean of {round(avg_new,2)} and stdev of {round(stdev_new,2)}')
print('We can now recalculate percentiles and z scores using the new values')
for i in range(0, 11):
    z = (i - avg_new) / stdev_new
    percentile = stats.norm.cdf(z)
    print(f'A Value of {i} as a Z-score of {round(z,2)} and is in the {round(100 * percentile, 2)} Percentile of values')

print('There is a catch though, the system is designed to be centered at 5, so as more matches are played, things will stabilize and re-center')

dist = stats.norm(loc=5, scale=2.8)

for i in range(0, 11):
    z = (i - avg_new) / stdev_new
    percentile = stats.norm.cdf(z)
    new_rating = dist.ppf(percentile)
    print(f'A Value of {i} will settle at {round(new_rating, 2)}')


