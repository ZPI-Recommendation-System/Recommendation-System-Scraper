import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import mergeCPUData
import mergeGPUData
from entities import *
import pandas as pd

LAPTOPS_CSV = "../clear-laptops2.csv"
OFFERS_CSV = "../clear-offers2.csv"


def insert_all(session, laptops, offers):
    cpu_benchmarks = pd.read_csv('../CPU_UserBenchmarks.csv')
    cpu_benchmarks = mergeCPUData.assign_cpus_from_benchmarks(laptops, cpu_benchmarks)
    added_cpu_benchmarks = dict()

    for cpu_model, benchmark in cpu_benchmarks.items():
        if benchmark is None:
            continue
        benchmark = benchmark.Benchmark
        benchmark_url = benchmark.URL
        if benchmark_url not in added_cpu_benchmarks:
            cpu_benchmark_entity = BenchmarkEntity(
                type=benchmark.Type,
                brand=benchmark.Brand,
                model=benchmark.Model,
                url=benchmark_url,
                benchmark=benchmark.Benchmark,
                samples=benchmark.Samples
            )
            added_cpu_benchmarks[benchmark_url] = cpu_benchmark_entity

    session.add_all(list(added_cpu_benchmarks.values()))

    gpu_benchmarks = pd.read_csv('../GPU_UserBenchmarks.csv')
    gpu_benchmarks = mergeGPUData.assign_gpus_from_benchmarks(laptops, gpu_benchmarks)
    added_gpu_benchmarks = dict()

    for gpu_model, benchmark in gpu_benchmarks.items():
        if benchmark is None:
            continue
        benchmark = benchmark.Benchmark
        benchmark_url = benchmark.URL
        if benchmark_url not in added_gpu_benchmarks:
            gpu_benchmark_entity = BenchmarkEntity(
                type=benchmark.Type,
                brand=benchmark.Brand,
                model=benchmark.Model,
                url=benchmark_url,
                benchmark=benchmark.Benchmark,
                samples=benchmark.Samples
            )
            added_gpu_benchmarks[benchmark_url] = gpu_benchmark_entity

    session.add_all(list(added_gpu_benchmarks.values()))

    added_multimedia = dict()
    added_drive_types = dict()
    added_controls = dict()
    added_connections = dict()
    added_communications = dict()

    for index, row in laptops.iterrows():
        cpu_benchmark = cpu_benchmarks[row['Model procesora']]
        cpu_benchmark_entity = None if cpu_benchmark is None else added_cpu_benchmarks[cpu_benchmark.Benchmark.URL]
        processor_entity = ProcessorEntity(
            model=row['Model procesora'],
            series=row['Seria procesora'],
            cores=row['Liczba rdzeni procesora'],
            frequency=row['Taktowanie bazowe procesora'],
            benchmark_entity=cpu_benchmark_entity
        )

        session.add(processor_entity)

        gpu_benchmark = gpu_benchmarks[row['Model karty graficznej']]
        gpu_benchmark_entity = None if gpu_benchmark is None else added_gpu_benchmarks[gpu_benchmark.Benchmark.URL]
        graphics_entity = GraphicsEntity(
            graphicsCardModel=row['Model karty graficznej'],
            graphicsCardType=row['Rodzaj karty graficznej'],
            graphicsCardVRam=row['Pamięć karty graficznej'],
            benchmark_entity=gpu_benchmark_entity
        )

        session.add(graphics_entity)

        screen_entity = ScreenEntity(
            diagonalScreenInches=row['Przekątna ekranu'],
            resolution=row['Rozdzielczość (px)'],
            screenFinish=row['Powłoka matrycy'],
            screenType=row['Typ matrycy'],
            refreshRate=row['Odświeżanie matrycy'],
            touchScreen=row['Ekran dotykowy']
        )

        session.add(screen_entity)

        model_img_entities = []

        for image_url in row['Zdjęcia']:
            entity = ModelImgEntity(
                url=image_url
            )
            model_img_entities.append(entity)

        session.add_all(model_img_entities)

        multimedia_entities = []

        for multimedia in row['Multimedia']:
            if multimedia not in added_multimedia:
                entity = MultimediaEntity(
                    multimediaName=multimedia
                )
                added_multimedia[multimedia] = entity
                multimedia_entities.append(entity)

        session.add_all(multimedia_entities)

        drive_type_entities = []
        model_entity = ModelEntity()

        for drive_type in row['Typ napędu']:
            if drive_type not in added_drive_types:
                entity = DriveTypeEntity(
                    driveType=drive_type,
                    model_entity=[model_entity]
                )
                added_drive_types[drive_type] = entity
                drive_type_entities.append(entity)
            else:
                pass
                added_drive_types[drive_type].model_entity.append(model_entity)

        session.add_all(drive_type_entities)

        control_entities = []

        for control in row['Sterowanie']:
            if control not in added_controls:
                entity = ControlEntity(
                    controlName=control,
                    model_entity=[model_entity]
                )
                added_controls[control] = entity
                control_entities.append(entity)
            else:
                added_controls[control].model_entity.append(model_entity)

        session.add_all(control_entities)

        connection_entities = []

        for connection in row['Złącza']:
            if connection not in added_connections:
                entity = ConnectionEntity(
                    connectionName=connection,
                    model_entity=[model_entity]
                )
                added_connections[connection] = entity
                connection_entities.append(entity)
            else:
                added_connections[connection].model_entity.append(model_entity)

        session.add_all(connection_entities)

        communication_entities = []

        for communication in row['Komunikacja']:
            if communication not in added_communications:
                entity = CommunicationEntity(
                    communicationName=communication,
                    model_entity=[model_entity]
                )
                added_communications[communication] = entity
                communication_entities.append(entity)
            else:
                added_communications[communication].model_entity.append(model_entity)

        session.add_all(communication_entities)

        model_entity.id = row['ID']
        model_entity.name = row['Name']
        model_entity.model = row['Model']
        model_entity.type = row['Typ']
        model_entity.producentCode = row['Kod producenta']
        model_entity.batterySizeWH = row['Pojemność akumulatora (Wh)']
        model_entity.batterySizeMAH = row['Pojemność akumulatora (mAh)']
        model_entity.batteryTime = row['Maksymalny czas pracy baterii']
        # model_entity.drive = "?"  # TODO drive?
        model_entity.color = row['Kolor']
        model_entity.width = row['Szerokość produktu']
        model_entity.length = row['Wysokość produktu']
        model_entity.depth = row['Głębokość produktu']
        model_entity.weight = row['Waga produktu']
        model_entity.ramAmount = row['Wielkość pamięci RAM']
        model_entity.ramFrequency = row['Częstotliwość taktowania pamięci (MHz)']
        model_entity.ramMaxAmount = row['Maksymalna wielkość pamięci RAM']
        model_entity.ramType = row['Typ pamięci RAM']
        model_entity.ramNumberOfSlots = row['Liczba slotów RAM']
        model_entity.ramNumberOfFreeSlots = row['Liczba wolnych slotów RAM']
        model_entity.driveStorage = row['Pojemność dysku']
        model_entity.driveType = row['Typ dysku twardego']
        model_entity.hddSpeed = row['Prędkość obrotowa dysku HDD']
        model_entity.processor_entity = processor_entity
        model_entity.graphics_entity = graphics_entity
        model_entity.screen_entity = screen_entity
        model_entity.multimedia_entity = multimedia_entities
        model_entity.model_img_entity = model_img_entities

        session.add(model_entity)

        model_offers = offers.loc[offers['Name'] == row['Name']]

        for index, offer in model_offers.iterrows():

            offer_entity = OfferEntity(
                offerName=offer['Name'],
                offerPrice=offer['Price'],
                offerURL=offer['URL'],
                model_entity=model_entity
            )
            session.add(offer_entity)

    print("Commit started...")
    session.commit()
    print("Commit finished!")


def delete_all(metadata, engine):
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())


def post_filter():
    clear_laptops = pd.read_csv(LAPTOPS_CSV)
    clear_offers = pd.read_csv(OFFERS_CSV)

    clear_offers['Price'] = clear_offers['Price'] \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: int(eval(x.split(' ')[0])))

    list_columns = {'Komunikacja', 'Złącza', 'Multimedia', 'Sterowanie', 'Typ napędu', 'Zdjęcia'}

    to_trim_columns = set(clear_laptops.columns.tolist()) - list_columns - {'ID', 'Name'}

    for col in to_trim_columns:
        clear_laptops[col] = clear_laptops[col].str.replace("^\\['", '', regex=True).replace("'\\]$", '', regex=True)

    for col in list_columns:
        clear_laptops[col] = clear_laptops[col] \
            .apply(str) \
            .apply(lambda x: [] if x == 'nan' else eval(x)) \
            .apply(lambda x: [] if 'brak' in x and len(x) > 1 else x)

    # rows_to_drop = clear_laptops[clear_laptops['Zdjęcia'].map(lambda x: len(x)) == 0]
    # clear_laptops = clear_laptops.drop(rows_to_drop.index)
    clear_laptops = clear_laptops[clear_laptops['Zdjęcia'].map(lambda x: len(x)) > 0]

    # string_columns = {'Typ', 'Kod producenta', 'Rozdzielczość (px)', 'Powłoka matrycy', 'Typ matrycy',
    #                   'Seria procesora', 'Seria procesora', 'Typ pamięci RAM', 'Typ dysku twardego', 'Kolor'}

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

    # TODO typ pola (wartość: współdzielona) i jaka min wielkosc
    # clear_laptops['Pamięć karty graficznej'] = clear_laptops['Pamięć karty graficznej'] \
    #     .apply(str) \
    #     .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' or x == 'współdzielona' else eval(x.split(' ')[0]) * 1024 if x.split(' ')[1] == "GB" else eval(x.split(' ')[0]))

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

    # int_columns = {'Odświeżanie matrycy', 'Pamięć karty graficznej', 'Liczba rdzeni procesora',
    #                'Maksymalna wielkość pamięci RAM', 'Częstotliwość taktowania pamięci (MHz)', 'Liczba slotów RAM',
    #                'Liczba wolnych slotów RAM', 'Pojemność dysku'}

    int_columns = {'Częstotliwość taktowania pamięci (MHz)', 'Liczba slotów RAM',
                   'Liczba wolnych slotów RAM'}

    for col in int_columns:
        clear_laptops[col] = clear_laptops[col] \
            .apply(str) \
            .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' else eval(x))

    # float_columns = {'Przekątna ekranu', 'Taktowanie bazowe procesora', 'Wielkość pamięci RAM',
    #                  'Pojemność akumulatora (Wh)', 'Pojemność akumulatora (mAh)', 'Maksymalny czas pracy baterii',
    #                  'Szerokość produktu', 'Wysokość produktu', 'Głębokość produktu', 'Waga produktu'}

    # TODO min wartość
    clear_laptops['Przekątna ekranu'] = clear_laptops['Przekątna ekranu'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(lambda x: x.split(' ')) \
        .apply(lambda x: sqlalchemy.sql.null() if eval(x[0]) < 11.6 else eval(x[0]))

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

    # for col in float_columns:
    #     clear_laptops[col] = clear_laptops[col] \
    #         .apply(str) \
    #         .apply(lambda x: sqlalchemy.sql.null() if x == 'nan' else eval(x))

    clear_laptops['Ekran dotykowy'] = clear_laptops['Ekran dotykowy'] \
        .apply(str) \
        .apply(lambda x: True if x == 'Tak' else False)

    return clear_laptops, clear_offers


if __name__ == "__main__":
    laptops, offers = post_filter()
    engine = create_engine('postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system')
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # delete_all(metadata, engine)
    insert_all(session, laptops, offers)
