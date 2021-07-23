class Maps:
    Assault = 'Assault'
    Control = 'Control'
    Escort = 'Escort'
    Hybrid = 'Hybrid'

    Hanamura = 'Hanamura'
    HorizonLunarColony = 'Horizon Lunar Colony'
    Paris = 'Paris'
    TempleOfAnubis = 'Temple of Anubis'
    VolskayaIndustries = 'Volskaya Industries'
    Busan = 'Busan'
    Ilios = 'Ilios'
    LijiangTower = 'Lijiang Tower'
    Nepal = 'Nepal'
    Oasis = 'Oasis'
    Dorado = 'Dorado'
    Havana = 'Havana'
    Junkertown = 'Junkertown'
    Rialto = 'Rialto'
    Route66 = 'Route 66'
    Gibraltar = 'Watchpoint: Gibraltar'
    Numbani = 'Numbani'
    Eichenwalde = 'Eichenwalde'
    KingsRow = 'King\'s Row'
    Hollywood = 'Hollywood'
    BlizzardWorld = 'Blizzard World'

    map_types = {
        Hanamura: Assault,
        HorizonLunarColony: Assault,
        Paris: Assault,
        TempleOfAnubis: Assault,
        VolskayaIndustries: Assault,

        Busan: Control,
        Ilios: Control,
        LijiangTower: Control,
        Nepal: Control,
        Oasis: Control,

        Dorado: Escort,
        Havana: Escort,
        Junkertown: Escort,
        Rialto: Escort,
        Route66: Escort,
        Gibraltar: Escort,

        Numbani: Hybrid,
        Eichenwalde: Hybrid,
        KingsRow: Hybrid,
        Hollywood: Hybrid,
        BlizzardWorld: Hybrid,
    }

    # Hybrid maps first point distance is given the distance from point 1-2
    map_dist = {
        (BlizzardWorld, 0): 0.0,
        (BlizzardWorld, 1): 127.5192413330078,
        (BlizzardWorld, 2): 127.5192413330078,
        (BlizzardWorld, 3): 111.63501739501952,
        (Dorado, 0): 0.0,
        (Dorado, 1): 127.5192413330078,
        (Dorado, 2): 127.5192413330078,
        (Dorado, 3): 111.63501739501952,
        (Eichenwalde, 0): 0.0,
        (Eichenwalde, 1): 127.5192413330078,
        (Eichenwalde, 2): 127.5192413330078,
        (Eichenwalde, 3): 111.63501739501952,
        (Havana, 0): 0.0,
        (Havana, 1): 127.5192413330078,
        (Havana, 2): 127.5192413330078,
        (Havana, 3): 111.63501739501952,
        (Hollywood, 0): 0.0,
        (Hollywood, 1): 127.5192413330078,
        (Hollywood, 2): 127.5192413330078,
        (Hollywood, 3): 111.63501739501952,
        (Junkertown, 0): 0.0,
        (Junkertown, 1): 127.5192413330078,
        (Junkertown, 2): 127.5192413330078,
        (Junkertown, 3): 111.63501739501952,
        (KingsRow, 0): 0.0,
        (KingsRow, 1): 127.5192413330078,
        (KingsRow, 2): 127.5192413330078,
        (KingsRow, 3): 111.63501739501952,
        (Numbani, 0): 0.0,
        (Numbani, 1): 127.5192413330078,
        (Numbani, 2): 127.5192413330078,
        (Numbani, 3): 111.63501739501952,
        (Rialto, 0): 0.0,
        (Rialto, 1): 127.5192413330078,
        (Rialto, 2): 127.5192413330078,
        (Rialto, 3): 111.63501739501952,
        (Route66, 0): 0.0,
        (Route66, 1): 127.5192413330078,
        (Route66, 2): 127.5192413330078,
        (Route66, 3): 111.63501739501952,
        (Gibraltar, 0): 0.0,
        (Gibraltar, 1): 127.5192413330078,
        (Gibraltar, 2): 127.5192413330078,
        (Gibraltar, 3): 111.63501739501952
    }


# TODO Implement OT rules
def time_to_add(map_type, point):
    if map_type == Maps.Assault:
        if point == 0:
            return 4 * 60
        elif point == 1:
            return 4 * 60
        elif point % 2 != 0:
            return 30
    if map_type == Maps.Hybrid or map_type == Maps.Escort:
        if point == 0:
            return 4 * 60
        elif point == 1:
            return 2.5 * 60
        elif point == 2:
            return 1.5 * 60
        else:
            return 0

    return 0


def total_map_time(map_type, point):
    total_time = 0
    for i in range(0, point + 1):
        total_time += time_to_add(map_type, i)
    return total_time


def total_escort_map_distance(map_name, point):
    dist = 0.0
    for i in range(0, point + 1):
        if i > 3:
            point_to_check = i % 3
        else:
            point_to_check = i
        dist += Maps.map_dist[(map_name, point_to_check)]
    return dist

def calc_map_type(map_name):
    return Maps.map_types[map_name]