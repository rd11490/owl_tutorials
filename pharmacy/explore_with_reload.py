import random
import matplotlib.pyplot as plt


tick_rate = 100


# (falloff start, falloff end, damage, recover (s), reload(s), ammo, id
ashe_asd = (30, 50, 75, .65, 3.5, 12, 'Ashe ASD')
ashe_hip = (20, 40, 40, .25, 3.5, 12, 'Ashe Hip Fire')
mccree = (20, 40, 70, .5, 1.5, 6, 'McCree')
baptiste = (25, 45, 24*3, .58, 1.5, 15, 'Baptiste')

soldier = (30, 50, 19, 1/9, 1.55, 30, 'Soldier')

# Constant for mercy's healing per second
mercy_healing = 55
mercy_healing_rate = mercy_healing / tick_rate
phara_health = 200



def calculate_falloff_rate(hero_stats, falloff_max):
    return (1 - falloff_max) / (hero_stats[0] - hero_stats[1])


def calculate_shot_damage(hero_stats, distance, crit_rate, falloff_max):
    damage = hero_stats[2] + (hero_stats[2] * crit_rate)
    if distance <= hero_stats[0]:
        return damage
    elif hero_stats[0] < distance <= hero_stats[1]:
        return damage * (1+(distance - hero_stats[0]) * calculate_falloff_rate(hero_stats, falloff_max))
    else:
        return damage * falloff_max


def true_ttk_at_distance(hero_stats, distance, crit_rate, falloff_max):
    x = [0]
    y = [phara_health]
    shots = hero_stats[5]
    reload = False
    reload_time = 0
    shot_damage = calculate_shot_damage(hero_stats, distance, crit_rate, falloff_max)
    for tick in range(1, 20 * tick_rate):
        x.append(tick)
        if (tick - 1) % int(hero_stats[3] * tick_rate) == 0.0 and not reload:
            damage_done = shot_damage
            shots -= 1


            if shots == 0:
                reload = True
                reload_time = tick + hero_stats[4] * tick_rate

        else:
            damage_done = 0

        pharah_current_health = round(y[tick-1] - damage_done + mercy_healing_rate, 3)

        if pharah_current_health < 0:
            pharah_current_health = 0
        if pharah_current_health > 200:
            pharah_current_health = 200
        y.append(pharah_current_health)

        if reload and tick >= reload_time:
            reload = False
            shots = 12

        if y[tick] <= 0:
            break

    return x[-1]


def true_ttk(hero_stats):
    print('\n')
    print(hero_stats[6])
    plt.figure(figsize=(10, 6))
    for falloff in [0.3, 0.5]:
        if falloff == 0.3:
            linestyle = 'solid'
        else:
            linestyle = 'dashed'
        for cr in [0.0, 0.5, 1.0]:
            if cr == 0.0:
                color = 'k'
            if cr == 0.5:
                color = 'g'
            if cr == 1.0:
                color = 'r'
            x = []
            y = []
            max_dist = 0
            ttk_end = 0
            for i in range(0, 80):
                ttk = true_ttk_at_distance(hero_stats, i, cr, falloff)
                x.append(i)
                y.append(ttk/tick_rate)
                if ttk < (tick_rate*20 - 1):
                    max_dist = i
                    ttk_end = ttk
            if max_dist > 0:
                print('At a distance of {0} Meters, crit rate of {1}, and a falloff of {2}, {3} can kill a Pharah with a mercy pocket after {4} seconds'.format(max_dist, cr, falloff, hero_stats[6], round(float(ttk_end)/tick_rate, 3)))
            plt.plot(x, y, linestyle=linestyle, color=color, label='{0} ({1} % crit rate, {2} falloff)'.format(hero_stats[6], cr*100, falloff))

    plt.legend()
    plt.xlim(0, 80)
    plt.ylim(0, 20)
    plt.title('{} Time to Kill Pharah'.format(hero_stats[6]))
    plt.xlabel('Distance (meters)')
    plt.ylabel('Time to Kill (seconds)')
    file_name = '_'.join(hero_stats[6].split(' '))
    plt.savefig('reload_results/{}.png'.format(file_name))





for hero in [ashe_hip, ashe_asd, mccree, soldier, baptiste]:
    true_ttk(hero)
