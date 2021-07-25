import matplotlib.pyplot as plt

# Constant for mercy's healing per second
mercy_healing = 55

# Maximum falloff multiplier
falloff_max = 0.3


# Tuple representing basic character information relevant to this script
# (Range at which falloff starts, Range for maximum falloff, base damage per shot, shots per second, identifier)
ashe_hip_falloff = (20, 40, 40, 4, 'Ashe Hip Fire')
ashe_ads_falloff = (30, 50, 75, 1 / .65, 'Ashe ADS')
baptiste_falloff = (25, 45, 24, 3 / .58, 'Baptiste')
mccree_falloff = (20, 40, 70, 2, 'McCree')
soldier_falloff = (30, 50, 19, 9, 'Soldier')


# Calculate the rate of change
def rate(xmin, xmax, ymin, ymax):
    return (ymax - ymin) / (xmax - xmin)

# Plot the falloff
def plot_damage_fallof(hero_stats):
    # Initialize two figures
    # Figure 1 is the hero dps figure
    fig1 = plt.figure(1, figsize=(10, 6))
    # Figure 2 is the time to kill figure
    fig2 = plt.figure(2, figsize=(10, 6))

    # Plot Mercy's healing per second on the DPS figure
    plt.figure(1)
    mercy_x = [0, 80]
    mercy_y = [mercy_healing, mercy_healing]
    plt.plot(mercy_x, mercy_y, label='Mercy HPS', color='k')

    # We want to show the impact across multiple crit rates. We will show what would happen
    # if the hero hits only body shots, 50% headshots, and 100% headshots
    for crit_accuracy in [0.0, 0.5, 1.0]:

        # Set a color per crit rate so that the color is consistent across plots
        if crit_accuracy == 0.0:
            color = 'r'
        elif crit_accuracy == 0.5:
            color = 'g'
        elif crit_accuracy == 1.0:
            color = 'b'

        # Calculate the base hero damage per second
        base_damage = hero_stats[2] * hero_stats[3]
        # Add in additional damage for head shots
        damage = base_damage + (base_damage * crit_accuracy)

        # Initial point on the graph
        zero = (0, damage)
        # Start of the ramp down due to falloff
        first = (hero_stats[0], damage)
        # End of the ramp down due to falloff
        second = (hero_stats[1], damage * falloff_max)
        # End of the graph
        third = (80, damage * falloff_max)

        # Calculate the falloff rate for the hero
        falloff_rate = rate(hero_stats[0], hero_stats[1], damage, damage * falloff_max)

        # Create an array of x values between the start and end of the falloff ramp down
        ramp_x = list(range(hero_stats[0], hero_stats[1]))
        # Calculate the damage at each meter in the ramp down
        ramp_y = [damage + (falloff_rate * (x - hero_stats[0])) for x in ramp_x]

        # Combine our lists together for one large plot
        x = [zero[0], first[0]] + ramp_x + [second[0], third[0]]
        y = [zero[1], first[1]] + ramp_y + [second[1], third[1]]

        # Plot DPS/HPS
        plt.figure(1)
        plt.plot(x, y, label='{0} DPS ({1} crit rate)'.format(hero_stats[4], crit_accuracy), color=color)

        plt.xlim((0, 80))
        plt.ylim((0, 300))
        plt.title('{0} Damage Per Second'.format(hero_stats[4]))
        plt.xlabel('Distance (meters)')
        plt.ylabel('Damage (Healing) per Second')

        plt.legend()

        # Plot TTK
        plt.figure(2)
        x_ttk = x
        y_mercy_ttk = [200 / max(dps - mercy_healing, 0.1) for dps in y]
        y_ttk = [200 / dps for dps in y]

        plt.plot(x_ttk, y_mercy_ttk, label='TTK with Mercy ({} crit rate)'.format(crit_accuracy), color=color)
        plt.plot(x_ttk, y_ttk, label='TTK with out Mercy ({} crit rate)'.format(crit_accuracy), color=color, linestyle='dashed')

        plt.xlim((0, 80))
        plt.ylim((0, 10))
        plt.title('{0} Time to Kill Pharah'.format(hero_stats[4]))
        plt.xlabel('Distance (meters)')
        plt.ylabel('Time to Kill (seconds)')
        plt.legend()

    plt.figure(1)
    plt.savefig('results/{0}.png'.format('_'.join(hero_stats[4].split(' '))))
    plt.figure(2)
    plt.savefig('results/{0}_ttk.png'.format('_'.join(hero_stats[4].split(' '))))
    plt.close(fig1)
    plt.close(fig2)


for hero in [ashe_hip_falloff, ashe_ads_falloff, mccree_falloff, soldier_falloff, baptiste_falloff]:
    plot_damage_fallof(hero)
