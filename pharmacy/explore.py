# Constant for mercy's healing per second
mercy_healing = 55

falloff_max = 0.3

# Tuple representing basic character information relevant to this script
# (Range at which falloff starts, Range for maximum falloff, base damage per shot, shots per second, identifier)
ashe_hip_falloff = (20, 40, 40, 4, 'Ashe Hip Fire')
ashe_asd_falloff = (30, 50, 75, 1 / .65, 'Ashe ASD')
baptiste_falloff = (25, 45, 24, 3 / .58, 'Baptiste')
mccree_falloff = (20, 40, 70, 2, 'McCree')
soldier_falloff = (30, 50, 19, 9, 'Soldier')


# Calculate the rate of change
def rate(xmin, xmax, ymin, ymax):
    return (ymax - ymin) / (xmax - xmin)


def explore_data(hero_stats, crit_accuracy):
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

    # Find the range at which the hero DPS is less than mercy HPS
    ineffective_list = [i for i, j in enumerate(y) if j < mercy_healing]
    if len(ineffective_list) > 0:
        print('Range at which {} can no longer kill Pharmacy with a crit rate of {}%: {} meters'.format(hero_stats[4],
                                                                                                        crit_accuracy * 100,
                                                                                                        x[
                                                                                                            ineffective_list[
                                                                                                                0]]))
    else:
        print(
            'There is no range at which {} can not overcome mercy healing to kill Pharmacy with a crit rate of {}%'.format(
                hero_stats[4], crit_accuracy * 100))
        new_ttk = round(200 / (damage * 0.3), 3)
        old_ttk = round(200 / (damage * 0.5), 3)
        print('Due to the change Pharmacy TTK has increased from {}s to {}s at max falloff'.format(old_ttk, new_ttk))


for hero in [ashe_hip_falloff, ashe_asd_falloff, mccree_falloff, soldier_falloff, baptiste_falloff]:
    print('\n')
    print(hero[4])
    for cr in [0.0, 0.5, 1.0]:
        print()
        explore_data(hero, cr)
