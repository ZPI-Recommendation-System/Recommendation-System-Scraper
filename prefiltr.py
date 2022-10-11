import pandas as pd


def clean_data():
    data = pd.read_excel("laptops.xlsx")
    display_condition = data['Przekątna ekranu'].isnull()
    cpu_condition = (data['Seria procesora'].isnull()) | (data['Model procesora'].isnull()) | (data['Liczba rdzeni procesora'].isnull()) | (data['Liczba rdzeni procesora'] == "['0']") | (data['Taktowanie bazowe procesora'].isnull()) | (data['Taktowanie bazowe procesora'] == "['0 GHz']")
    gpu_condition = (data['Rodzaj karty graficznej'].isnull()) | (data['Rodzaj karty graficznej'] == "['brak informacji']") | (data['Model karty graficznej'].isnull())
    ram_condition = (data['Wielkość pamięci RAM'].isnull()) | (data['Wielkość pamięci RAM'] == "['0 GB']") | (data['Wielkość pamięci RAM'] == "['brak']")
    hard_drive_condition = (data['Typ dysku twardego'].isnull()) | (data['Pojemność dysku'].isnull()) | (data['Pojemność dysku'] == "['0 GB']") | (data['Typ dysku twardego'] == "['brak']")
    # connectors_condition = data['Złącza'].isnull()
    battery_condition = data['Maksymalny czas pracy baterii'].isnull()
    condition = display_condition | cpu_condition | gpu_condition | ram_condition | hard_drive_condition | battery_condition#connectors_condition
    rows_to_drop = data[condition]
    filtered_data = data.drop(rows_to_drop.index)
    pd.DataFrame(filtered_data).to_excel("prefilter-output.xlsx", encoding='utf-8', index=False)


if __name__ == "__main__":
    clean_data()
