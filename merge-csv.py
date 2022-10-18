# 0. Po pobraniu danych scraperem prefiltrujemy; dodać do scrapera drop kolumn
# 1. Wczytujemy csv laptopów i ofert
# 2. Bierzemy nazwe oferty i szukamy wsrod laptopow. Jesli pokazuje nam kilka to bierzemy pierwszy z brzegu.
# 3. Dodajemy laptopa i oferte do nowej kolekcji. Jeżeli nie znalazlo laptopa to pomijamy oferte.
# 4. Pakujemy dane do bazy
# model <-> oferta
#  [id laptopa; id_oferty] - oferta(id_oferty, cena, url)

import pandas as pd

LAPTOPS_CSV_FILE = "laptops.csv"
OFFERS_CSV_FILE = "21k_allegro_laptopy.csv"


def prefilter(laptops):
    # laptops = pd.read_excel("laptops.xlsx")
    display_condition = laptops['Przekątna ekranu'].isnull()
    cpu_condition = (laptops['Seria procesora'].isnull()) | ("Inny procesor(" in laptops['Seria procesora']) | (laptops['Model procesora'].isnull()) | (laptops['Liczba rdzeni procesora'].isnull()) | (laptops['Liczba rdzeni procesora'] == "['0']") | (laptops['Taktowanie bazowe procesora'].isnull()) | (laptops['Taktowanie bazowe procesora'] == "['0 GHz']")
    gpu_condition = (laptops['Rodzaj karty graficznej'].isnull()) | (laptops['Rodzaj karty graficznej'] == "['brak informacji']") | (laptops['Model karty graficznej'].isnull())
    ram_condition = (laptops['Wielkość pamięci RAM'].isnull()) | (laptops['Wielkość pamięci RAM'] == "['0 GB']") | (laptops['Wielkość pamięci RAM'] == "['brak']")
    hard_drive_condition = (laptops['Typ dysku twardego'].isnull()) | (laptops['Pojemność dysku'].isnull()) | (laptops['Pojemność dysku'] == "['0 GB']") | (laptops['Typ dysku twardego'] == "['brak']")
    # connectors_condition = laptops['Złącza'].isnull()
    battery_condition = laptops['Maksymalny czas pracy baterii'].isnull()
    condition = display_condition | cpu_condition | gpu_condition | ram_condition | hard_drive_condition | battery_condition #connectors_condition
    rows_to_drop = laptops[condition]
    filtered_data = laptops.drop(rows_to_drop.index)
    # pd.DataFrame(filtered_data).to_excel("prefilter-output.xlsx", encoding='utf-8', index=False)
    return filtered_data



def merge():
    # 1. scraper (usuwa niepotrzebne kolumny)
    laptops = pd.read_csv(LAPTOPS_CSV_FILE)
    laptops = prefilter(laptops)
    offers = pd.read_csv(OFFERS_CSV_FILE, on_bad_lines='skip', sep='\t', names=['Name', 'Price', 'URL', 'Category'], header=None)
    offers['Name'] = offers['Name'].str.replace("^'", '', regex=True).replace("'$", '', regex=True).to_list()
    laptops['Name'] = laptops['Name'].str.replace('^"', '', regex=True).replace('"$', '', regex=True).to_list()
    merged_data = pd.merge(laptops, offers, on='Name', how='inner')
    offers = merged_data[['Name', 'Price', 'URL', 'Category']]
    offers.to_csv("clear-offers.csv", index=False, header=True)
    merged_data = merged_data.drop_duplicates(subset=['Name'])
    laptops = merged_data.drop(columns=['Price', 'URL', 'Category'])
    laptops.to_csv("clear-laptops.csv", index=False, header=True)


if __name__ == "__main__":
    merge()
