import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from statistics import median

from db.entities import *
from src import benchmarks, postfilter
from src.constants import CPU_BENCHMARKS_CSV, GPU_BENCHMARKS_CSV, DATABASE_URL
from src.merge_benchmarks.mergeCPUData import MergeAllegroCPU
from src.merge_benchmarks.mergeGPUData import MergeAllegroGPU

entities = [t_model_entity_communications_communication_entity, t_model_entity_connections_connection_entity, t_model_entity_controls_control_entity, t_model_entity_drives_drive_type_entity, t_model_entity_images_model_img_entity, t_model_entity_multimedia_multimedia_entity, t_model_entity_images_model_img_entity, ModelEntity, ModelImgEntity, CommunicationEntity, ConnectionEntity, ControlEntity, DriveTypeEntity, ScreenEntity, MultimediaEntity, GraphicsEntity, ProcessorEntity, BenchmarkEntity]


def insert_all(session, laptops, cpu_benchmarks, gpu_benchmarks):
    cpu_benchmarks = MergeAllegroCPU.print_assigns(laptops, cpu_benchmarks)
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

    gpu_benchmarks = MergeAllegroGPU.print_assigns(laptops, gpu_benchmarks)
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
        model_entity.price = row['price']
        model_priceSource = row['priceSource']
        model_entity.processor_entity = processor_entity
        model_entity.graphics_entity = graphics_entity
        model_entity.screen_entity = screen_entity
        model_entity.multimedia_entity = multimedia_entities
        model_entity.model_img_entity = model_img_entities

        session.add(model_entity)

    print("Commit started...")
    # session.commit()
    print("Commit finished!")


def delete_all(metadata, engine, session):
    # for table in reversed(metadata.sorted_tables):
    #     engine.execute(table.delete())
    try:
        for entity in entities:
            num_rows_deleted = session.query(entity).delete()
            print(num_rows_deleted)
    except:
        session.rollback()
        raise

def update(laptops, cpu_benchmarks, gpu_benchmarks):
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    delete_all(metadata, engine, session)
    insert_all(session, laptops, cpu_benchmarks, gpu_benchmarks)


if __name__ == "__main__":
    # laptops = pd.read_csv("clear-laptops2.csv")
    # offers = pd.read_csv("clear-offers2.csv")
    # laptops, offers = postfilter.run_for(laptops, offers)
    # cpu_benchmarks, gpu_benchmarks = benchmarks.get()
    # update(laptops, offers, cpu_benchmarks, gpu_benchmarks)

    laptops = pd.read_csv("clear-laptops2.csv")
    laptops = postfilter.run_for(laptops)
    cpu_benchmarks, gpu_benchmarks = benchmarks.get()
    update(laptops, cpu_benchmarks, gpu_benchmarks)
