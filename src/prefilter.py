def run_for(laptops):
    unused_columns = ['EAN (GTIN)', 'Taktowanie maksymalne procesora', 'Pamięć podręczna procesora', 'Interfejs dysku', 'Technologia akumulatora', 'Liczba komór akumulatora', 'Cechy dodatkowe', 'Materiał', 'Waga produktu z opakowaniem jednostkowym']
    laptops = laptops.drop(columns=unused_columns)
    laptops = laptops.drop_duplicates(subset=['ID'])

    id_condition = (laptops['ID'].isnull()) | (laptops['Name'].isnull()) | (laptops['Model'].isnull())
    display_condition = laptops['Przekątna ekranu'].isnull()
    # cpu_condition = (laptops['Seria procesora'].isnull()) | ("Inny procesor(" in laptops['Seria procesora']) | (laptops['Model procesora'].isnull()) | (laptops['Liczba rdzeni procesora'].isnull()) | (laptops['Liczba rdzeni procesora'] == "['0']") | (laptops['Taktowanie bazowe procesora'].isnull()) | (laptops['Taktowanie bazowe procesora'] == "['0 GHz']")
    cpu_condition = ("Inny procesor(" in laptops['Seria procesora']) | (laptops['Model procesora'].isnull())
    gpu_condition = (laptops['Rodzaj karty graficznej'].isnull()) | (laptops['Rodzaj karty graficznej'] == "['brak informacji']") | (laptops['Model karty graficznej'].isnull())
    # ram_condition = (laptops['Wielkość pamięci RAM'].isnull()) | (laptops['Wielkość pamięci RAM'] == "['0 GB']") | (laptops['Wielkość pamięci RAM'] == "['brak']")
    ram_condition = (laptops['Wielkość pamięci RAM'].isnull()) | ("brak" in laptops['Wielkość pamięci RAM'])
    # hard_drive_condition = (laptops['Typ dysku twardego'].isnull()) | (laptops['Pojemność dysku'].isnull()) | (laptops['Pojemność dysku'] == "['0 GB']") | (laptops['Typ dysku twardego'] == "['brak']")
    hard_drive_condition = (laptops['Pojemność dysku'].isnull())
    # battery_condition = laptops['Maksymalny czas pracy baterii'].isnull()
    # condition = id_condition | display_condition | cpu_condition | gpu_condition | ram_condition | hard_drive_condition | battery_condition #connectors_condition
    condition = id_condition | display_condition | cpu_condition | gpu_condition | ram_condition | hard_drive_condition
    rows_to_drop = laptops[condition]
    filtered_data = laptops.drop(rows_to_drop.index)
    return filtered_data
