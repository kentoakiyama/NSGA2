def get_problem(name: str):
    if name == 'TNK':
        from test_functions.tnk import TNK
        return TNK
    elif name == 'BNH':
        from test_functions.bnh import BNH
        return BNH
    elif name == 'KUR':
        from test_functions.kur import KUR
        return KUR
    elif name == 'ZDT2':
        from test_functions.zdt import ZDT2
        return ZDT2
    elif name == 'ZDT4':
        from test_functions.zdt import ZDT4
        return ZDT4
    elif name == 'OsyczkaKundu':
        from test_functions.osyczkakundu import OsyczkaKundu
        return OsyczkaKundu