import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

players = 40000000
comp_players = int(0.01 * players)
comp_players_ow1 = int(comp_players / 3)
comp_players_ow2 = int(2 * comp_players / 3)

sr_mean = 2500
sr_std = 750

new_sr_mean = 1500
new_sr_std = 750


def handle_edge(x):
    # if x > 5000:
    #     return int(np.random.randint(4500, 5000))
    # if x < 0:
    #     return int(np.random.randint(0, 1500))
    return int(x)

def build_fig():
    fig = plt.figure(figsize=(12, 6))
    plt.xlabel('MMR/SR)')
    plt.ylabel('# of Players')
    plt.title('Player Rank Distribution')
    plt.xlim(0, 5000)
    plt.ylim(0, 3000)
    return fig


comp_ratings_ow1 = [handle_edge(sr) for sr in np.random.normal(sr_mean, sr_std, comp_players_ow1)]
comp_ratings_ow1.append(0)
comp_ratings_ow1.append(5000)
comp_ratings_ow2_new = [handle_edge(sr) for sr in np.random.normal(new_sr_mean, new_sr_std, comp_players_ow2)]

comp_ratings_ow2 = comp_ratings_ow2_new + comp_ratings_ow1

bins = list(range(0, 5001, 10))

ow1_hist = np.histogram(comp_ratings_ow1, bins)

ratings_ow1 = ow1_hist[0]
counts_ow1 = ow1_hist[1][1:]

fig_ow1 = build_fig()
plt.plot(counts_ow1, ratings_ow1, label='OW1 Distribution', color='blue')
plt.legend()
plt.savefig('MMR_Distribution_OW1.png')

ow2_hist = np.histogram(comp_ratings_ow2_new, bins)
ratings_ow2_new = ow2_hist[0]
counts_ow2_new = ow2_hist[1][1:]

fig_ow2 = build_fig()
plt.plot(counts_ow1, ratings_ow1, label='OW1 Distribution', color='blue')
plt.plot(counts_ow2_new, ratings_ow2_new, label='OW2 New Players Distribution', color='black')
plt.legend()
plt.savefig('MMR_Distribution_OW2.png')

ow2_hist = np.histogram(comp_ratings_ow2, bins)
ratings_ow2_total = ow2_hist[0]
counts_ow2_total = ow2_hist[1][1:]

fig_ow3 = build_fig()
plt.plot(counts_ow1, ratings_ow1, label='OW1 Distribution', color='blue')
plt.plot(counts_ow2_new, ratings_ow2_new, label='OW2 New Players Distribution', color='black')
plt.plot(counts_ow2_total, ratings_ow2_total, label='OW2 Total Distribution', color='red')
plt.legend()
plt.savefig('MMR_Distribution_total.png')

mean = np.mean(comp_ratings_ow2)
stdev = np.std(comp_ratings_ow2)

dist = stats.norm(loc=sr_mean, scale=sr_std)

comp_ratings_ow2_adjusted = []

for sr in sorted(comp_ratings_ow2):
    z = (sr - mean) / stdev
    percentile = stats.norm.cdf(z)
    new_rating = dist.ppf(percentile)
    comp_ratings_ow2_adjusted.append(new_rating)

ow2_adjusted_hist = np.histogram(comp_ratings_ow2_adjusted, bins)
ratings_adjusted = ow2_adjusted_hist[0]
counts_adjusted = ow2_adjusted_hist[1][1:]


bins = list(range(1000, 4500, 250))
for sr in bins:
    z = (sr - mean) / stdev
    percentile = stats.norm.cdf(z)
    new_rating = dist.ppf(percentile)

    z_old = (sr - sr_mean) / sr_std
    percentile_old = stats.norm.cdf(z_old)
    print(
        f'An SR of {sr} ({round(percentile_old,2)} in OW1) in OW2 will roughly translates to an SR of {round(new_rating,2)} ({round(percentile,2)} in OW2) in OW1 once ranks have settled')

z = (2500 - mean) / stdev
percentile_2500 = stats.norm.cdf(z)
new_rating_2500 = dist.ppf(percentile_2500)

z = (3500 - mean) / stdev
percentile_3500 = stats.norm.cdf(z)
new_rating_3500 = dist.ppf(percentile_3500)

fig_final = build_fig()
plt.plot(counts_ow1, ratings_ow1, label='OW1 Distribution', color='blue')
plt.plot(counts_ow2_new, ratings_ow2_new, label='OW2 New Players Distribution', color='black')
plt.plot(counts_ow2_total, ratings_ow2_total, label='OW2 Total Distribution', color='red')
plt.plot(counts_adjusted, ratings_adjusted, label='OW2 Settled Distribution', color='green')

plt.plot([3500, 3500], [0, 5000], color='orange', linestyle='dashed')
plt.plot([new_rating_3500, new_rating_3500], [0, 5000], color='orange', linestyle='dashed', label='3500 OW1 player')

text_x = (3500 + new_rating_3500) / 2

plt.text(text_x, 2500, f'A 3500 Player\nin OW1 should\neventually settle\nat {int(new_rating_3500)} in OW2', color='k',
         wrap=True, horizontalalignment='center')

plt.plot([2500, 2500], [0, 5000], color='purple', linestyle='dashed')
plt.plot([new_rating_2500, new_rating_2500], [0, 5000], color='purple', linestyle='dashed', label='2500 OW1 player')
text_x = (2500 + new_rating_2500) / 2

plt.text(text_x, 2500, f'A 2500 Player\nin OW1 should\neventually settle\nat {int(new_rating_2500)} in OW2', color='k',
         wrap=True, horizontalalignment='center')

plt.legend()
plt.savefig('MMR_Distribution.png')
