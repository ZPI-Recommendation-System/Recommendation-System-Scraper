# coding: utf-8
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CommunicationEntity(Base):
    __tablename__ = 'communication_entity'

    communicationName = Column(String, primary_key=True)

    model_entity = relationship('ModelEntity', secondary='model_entity_communications_communication_entity')


class ConnectionEntity(Base):
    __tablename__ = 'connection_entity'

    connectionName = Column(String, primary_key=True)

    model_entity = relationship('ModelEntity', secondary='model_entity_connections_connection_entity')


class ControlEntity(Base):
    __tablename__ = 'control_entity'

    controlName = Column(String, primary_key=True)

    model_entity = relationship('ModelEntity', secondary='model_entity_controls_control_entity')


class GraphicsEntity(Base):
    __tablename__ = 'graphics_entity'

    graphicsCardModel = Column(String, primary_key=True)
    graphicsCardType = Column(String)
    graphicsCardVRam = Column(Integer)


class MultimediaEntity(Base):
    __tablename__ = 'multimedia_entity'

    multimediaName = Column(String, primary_key=True)


class ProcessorEntity(Base):
    __tablename__ = 'processor_entity'

    model = Column(String, primary_key=True)
    series = Column(String, nullable=False)
    cores = Column(Integer, nullable=False)
    frequency = Column(Float(53), nullable=False)


class RamEntity(Base):
    __tablename__ = 'ram_entity'

    ramId = Column(Integer, primary_key=True, server_default=text("nextval('\"ram_entity_ramId_seq\"'::regclass)"))
    ramAmount = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)
    numberOfSlots = Column(Integer, nullable=False)
    numberOfFreeSlots = Column(Integer, nullable=False)
    ramType = Column(String, nullable=False)


class ScreenEntity(Base):
    __tablename__ = 'screen_entity'

    screenId = Column(Integer, primary_key=True, server_default=text("nextval('\"screen_entity_screenId_seq\"'::regclass)"))
    diagonalScreenInches = Column(Float(53), nullable=False)
    resolution = Column(String, nullable=False)
    screenFinish = Column(String, nullable=False)
    screenType = Column(String, nullable=False)
    refreshRate = Column(Integer, nullable=False)
    touchScreen = Column(Boolean, nullable=False)


class StorageEntity(Base):
    __tablename__ = 'storage_entity'

    driveId = Column(Integer, primary_key=True, server_default=text("nextval('\"storage_entity_driveId_seq\"'::regclass)"))
    driveStorage = Column(Integer, nullable=False)
    driveType = Column(String, nullable=False)
    hddSpeed = Column(String)


class ModelEntity(Base):
    __tablename__ = 'model_entity'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    type = Column(String, nullable=False)
    processorModel = Column(ForeignKey('processor_entity.model'))
    producentCode = Column(String)
    batterySizeWH = Column(Integer)
    batterySizeMAH = Column(Integer)
    batteryTime = Column(Integer)
    drive = Column(String, nullable=False)
    color = Column(String)
    width = Column(Integer)
    length = Column(Integer)
    depth = Column(Integer)
    weight = Column(Integer)
    screenScreenId = Column(ForeignKey('screen_entity.screenId'))
    ramRamId = Column(ForeignKey('ram_entity.ramId'))
    storageDriveId = Column(ForeignKey('storage_entity.driveId'))
    graphicsGraphicsCardModel = Column(ForeignKey('graphics_entity.graphicsCardModel'))

    graphics_entity = relationship('GraphicsEntity')
    processor_entity = relationship('ProcessorEntity')
    ram_entity = relationship('RamEntity')
    screen_entity = relationship('ScreenEntity')
    storage_entity = relationship('StorageEntity')
    multimedia_entity = relationship('MultimediaEntity', secondary='model_entity_multimedia_multimedia_entity')


t_model_entity_communications_communication_entity = Table(
    'model_entity_communications_communication_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('communicationEntityCommunicationName', ForeignKey('communication_entity.communicationName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_connections_connection_entity = Table(
    'model_entity_connections_connection_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('connectionEntityConnectionName', ForeignKey('connection_entity.connectionName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_controls_control_entity = Table(
    'model_entity_controls_control_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('controlEntityControlName', ForeignKey('control_entity.controlName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_multimedia_multimedia_entity = Table(
    'model_entity_multimedia_multimedia_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('multimediaEntityMultimediaName', ForeignKey('multimedia_entity.multimediaName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OfferEntity(Base):
    __tablename__ = 'offer_entity'

    offerId = Column(Integer, primary_key=True, server_default=text("nextval('\"offer_entity_offerId_seq\"'::regclass)"))
    offerName = Column(String, nullable=False)
    offerURL = Column(String, nullable=False)
    offerPrice = Column(Integer, nullable=False)
    modelId = Column(ForeignKey('model_entity.id'))

    model_entity = relationship('ModelEntity')
