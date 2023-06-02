
class Maps:
    Assault = 'Assault'
    Control = 'Control'
    Escort = 'Escort'
    Hybrid = 'Hybrid'
    Push = 'Push'

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
    NewQueenStreet = 'New Queen Street'
    Colosseo = 'Colosseo'
    Midtown = 'Midtown'
    Paraiso = 'Paraíso'
    CircuitRoyal = 'Circuit royal'
    Esperanca = 'Esperança'
    AntarcticPeninsula = 'Antarctic Peninsula'
    Shambali = 'Shambali Monastery'

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
        AntarcticPeninsula: Control,

        Dorado: Escort,
        Havana: Escort,
        Junkertown: Escort,
        Rialto: Escort,
        Route66: Escort,
        Gibraltar: Escort,
        CircuitRoyal: Escort,
        Shambali: Escort,

        Numbani: Hybrid,
        Eichenwalde: Hybrid,
        KingsRow: Hybrid,
        Hollywood: Hybrid,
        BlizzardWorld: Hybrid,
        Midtown: Hybrid,
        Paraiso: Hybrid,

        NewQueenStreet: Push,
        Colosseo: Push,
        Esperanca: Push
    }


class Teams:
    Hunters = 'Chengdu Hunters'
    Charge = 'Guangzhou Charge'
    Spark = 'Hangzhou Spark'
    Valiant = 'Los Angeles Valiant'
    Excelsior = 'New York Excelsior'
    Fusion = 'Philadelphia Fusion'
    Dynasty = 'Seoul Dynasty'
    Dragons = 'Shanghai Dragons'
    Infernal = 'Seoul Infernal'

    Reign = 'Atlanta Reign'
    Uprising = 'Boston Uprising'
    Fuel = 'Dallas Fuel'
    Mayhem = 'Florida Mayhem'
    Outlaws = 'Houston Outlaws'
    Spitfire = 'London Spitfire'
    Gladiators = 'Los Angeles Gladiators'
    Eternal = 'Paris Eternal'
    VEternal = 'Vegas Eternal'
    Shock = 'San Francisco Shock'
    Defiant = 'Toronto Defiant'
    Titans = 'Vancouver Titans'
    Justice = 'Washington Justice'

    East21 = [Hunters, Charge, Spark, Valiant, Excelsior, Fusion, Dynasty, Dragons]
    West21 = [Reign, Uprising, Fuel, Mayhem, Outlaws, Spitfire, Gladiators, Eternal, Shock, Defiant, Titans, Justice]

    East22 = [Hunters, Charge, Spark, Valiant, Fusion, Dynasty, Dragons]
    West22 = [Reign, Uprising, Excelsior, Fuel, Mayhem, Outlaws, Spitfire, Gladiators, Eternal, Shock, Defiant, Titans,
              Justice]

    East23 = [Charge, Spark, Infernal, Dynasty, Dragons, Fuel]
    West23 = [Reign, Uprising, Excelsior, Valiant, Mayhem, Outlaws, Spitfire, Gladiators, VEternal, Shock, Defiant, Titans,
              Justice]

    TeamColors = {
        Reign: '#910F1B',
        Uprising: '#174B97',
        Hunters: '#FFA000',
        Fuel: '#0072CE',
        Mayhem: '#CF4691',
        Gladiators: '#3C1053',
        Charge: '#122C42',
        Outlaws: '#97D700',
        Spark: '#FB7299',
        Spitfire: '#59CBE8',
        Excelsior: '#171C38',
        Eternal: '#8D042D',
        Fusion: '#000000',
        Dynasty: '#AA8A00',
        Shock: '#A5ACAF',
        Dragons: '#D22630',
        Defiant: '#C10021',
        Valiant: '#FFD100',
        Titans: '#2FB228',
        Justice: '#990034',
        Infernal: '#000000',
        VEternal: '#8D042D'
    }