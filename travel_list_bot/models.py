from sqlalchemy import Column, Integer, String, Float, Text, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    longitude = Column(Float, nullable=True, unique=False)
    latitude = Column(Float, nullable=True, unique=False)
    photo_id = Column(String(128), nullable=True, unique=False)
    comment = Column(Text(length=512), nullable=True, unique=False)
    chat = relationship('Chat', back_populates='place')

    def __repr__(self):
        return f'<Place: name={self.name}, chat_id={self.chat_id}, ' +\
            f'long={self.longitude}, lat={self.latitude}, ' +\
            f'photo_id={self.photo_id}, comment={self.comment}>'


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    step = Column(Enum('-1', '0', '1', '2', '3'), unique=False, default='-1')
    place = relationship('Place', uselist=False, back_populates='chat')
    place_id = Column(Integer, ForeignKey('places.id'))

    def __repr__(self):
        return f'<Chat: id={self.id}, state={self.step}>'
