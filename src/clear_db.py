import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.entities import *
from src import websockets
from src.constants import DATABASE_URL
from src.websockets import emit_job_status

entities = [t_model_entity_communications_communication_entity, t_model_entity_connections_connection_entity, t_model_entity_controls_control_entity, t_model_entity_drives_drive_type_entity, t_model_entity_images_model_img_entity, t_model_entity_multimedia_multimedia_entity, t_model_entity_images_model_img_entity, ModelEntity, ModelImgEntity, CommunicationEntity, ConnectionEntity, ControlEntity, DriveTypeEntity, ScreenEntity, MultimediaEntity, GraphicsEntity, ProcessorEntity, BenchmarkEntity]


def run():
    emit_job_status(job='clear_db', status='running', logs=['Rozpoczęto operację czyszczenia bazy danych'])
    logging.info("Rozpoczęto operację uczenia modelu")
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        for entity in entities:
            num_rows_deleted = session.query(entity).delete()
        emit_job_status(job='clear_db', status='ok', logs=['Operacja zakończona pomyślnie'])
        logging.info("Operacja zakończona pomyślnie")
    except:
        session.rollback()
        logging.error("Operacja zakończona błędem", exc_info=True, stack_info=True)
        emit_job_status(job='clear_db', status='error', logs=['Operacja zakończona błędem'])

    websockets.isRunning = False
    websockets.job = ""

if __name__ == "__main__":
    run()
