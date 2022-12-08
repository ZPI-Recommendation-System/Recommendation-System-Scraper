import sqlalchemy


def run_for(clear_laptops):
    list_columns = {'Komunikacja', 'Złącza', 'Multimedia', 'Sterowanie', 'Typ napędu', 'Zdjęcia'}

    to_trim_columns = set(clear_laptops.columns.tolist()) - list_columns - {'ID', 'Name'}

    for col in to_trim_columns:
        clear_laptops[col] = clear_laptops[col].astype(str).str.replace("^\\['", '', regex=True).replace("'\\]$", '', regex=True)

    for col in list_columns:
        clear_laptops[col] = clear_laptops[col] \
            .apply(str) \
            .apply(lambda x: [] if x == 'nan' else eval(x)) \
            .apply(lambda x: [] if 'brak' in x and len(x) > 1 else x)

    clear_laptops.drop(clear_laptops[clear_laptops['Zdjęcia'].map(len) == 0].index, inplace=True)

    string_columns = {'Kod producenta', 'Rozdzielczość (px)', 'Powłoka matrycy', 'Typ matrycy',
                      'Seria procesora', 'Seria procesora', 'Typ pamięci RAM', 'Typ dysku twardego', 'Kolor',
                      'Pamięć karty graficznej'}

    for col in string_columns:
        clear_laptops[col] = clear_laptops[col] \
            .apply(str) \
            .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' else x)

    clear_laptops['Odświeżanie matrycy'] = clear_laptops['Odświeżanie matrycy'] \
        .apply(str) \
        .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' or eval(x.split(' Hz')[0]) < 60 else eval(x.split(' Hz')[0]))

    clear_laptops['Liczba rdzeni procesora'] = clear_laptops['Liczba rdzeni procesora'] \
        .apply(str) \
        .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' or x == 'nie dotyczy' else eval(x))

    # TODO min wartość i czy większa od RAM
    clear_laptops['Maksymalna wielkość pamięci RAM'] = clear_laptops['Maksymalna wielkość pamięci RAM'] \
        .apply(str) \
        .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' or x.split(' ')[1] == 'MB' else eval(x.split(' ')[0]))

    # TODO min wartość (jest 250 GB)
    clear_laptops['Pojemność dysku'] = clear_laptops['Pojemność dysku'] \
        .apply(str) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if eval(x[0]) < 250 else eval(x[0]))

    rows_to_drop = clear_laptops[clear_laptops['Pojemność dysku'] == sqlalchemy.sql.null()]
    clear_laptops = clear_laptops.drop(rows_to_drop.index)

    int_columns = {'Częstotliwość taktowania pamięci (MHz)', 'Liczba slotów RAM',
                   'Liczba wolnych slotów RAM', 'Prędkość obrotowa dysku HDD'}

    for col in int_columns:
        clear_laptops[col] = clear_laptops[col] \
            .apply(str) \
            .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' else eval(x))

    # TODO min wartość
    clear_laptops['Przekątna ekranu'] = clear_laptops['Przekątna ekranu'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if eval(x[0]) <= 7 else eval(x[0]))

    rows_to_drop = clear_laptops[clear_laptops['Przekątna ekranu'] == sqlalchemy.sql.null()]
    clear_laptops = clear_laptops.drop(rows_to_drop.index)

    # TODO min wartość
    clear_laptops['Taktowanie bazowe procesora'] = clear_laptops['Taktowanie bazowe procesora'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' or eval(x[0]) < 1 else eval(x[0]))

    # TODO min wartość
    clear_laptops['Wielkość pamięci RAM'] = clear_laptops['Wielkość pamięci RAM'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'brak' or x[1] == 'MB' or eval(x[0]) < 4 else eval(x[0]))

    rows_to_drop = clear_laptops[clear_laptops['Wielkość pamięci RAM'] == sqlalchemy.sql.null()]
    clear_laptops = clear_laptops.drop(rows_to_drop.index)

    # TODO min wartość
    clear_laptops['Pojemność akumulatora (Wh)'] = clear_laptops['Pojemność akumulatora (Wh)'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' else eval(x[0]))

    # TODO min wartość
    clear_laptops['Pojemność akumulatora (mAh)'] = clear_laptops['Pojemność akumulatora (mAh)'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' else eval(x[0]))

    # TODO min wartość; może też max?
    clear_laptops['Maksymalny czas pracy baterii'] = clear_laptops['Maksymalny czas pracy baterii'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' or eval(x[0]) < 2 else eval(x[0]))

    # TODO min i max wartość
    clear_laptops['Szerokość produktu'] = clear_laptops['Szerokość produktu'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' or eval(x[0]) < 7 or eval(x[0]) > 50 else eval(x[0]))

    # TODO min i max wartość
    clear_laptops['Wysokość produktu'] = clear_laptops['Wysokość produktu'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' or eval(x[0]) < 0.2 or eval(x[0]) > 8 else eval(x[0]))

    # TODO min i max wartość
    clear_laptops['Głębokość produktu'] = clear_laptops['Głębokość produktu'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' or eval(x[0]) < 1.5 or eval(x[0]) > 36 else eval(x[0]))

    # TODO min i max wartość
    clear_laptops['Waga produktu'] = clear_laptops['Waga produktu'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if x[0] == 'nan' or eval(x[0]) < 0.15 or eval(x[0]) > 5 else eval(x[0]))

    clear_laptops['Ekran dotykowy'] = clear_laptops['Ekran dotykowy'] \
        .apply(str) \
        .apply(lambda x: True if x == 'Tak' else False)

    return clear_laptops
