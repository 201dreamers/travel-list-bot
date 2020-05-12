from models import Place, Chat
from config.db import session


def db_get_places(chat_id, how_much):
    how_much = int(how_much)
    if how_much > 0:
        return session.query(Place).filter_by(chat_id=chat_id)\
            .order_by(Place.id).limit(how_much)
    elif how_much < 0:
        how_much = how_much * -1
        return session.query(Place).filter_by(chat_id=chat_id)\
            .order_by(Place.id.desc()).limit(how_much)
    else:
        return session.query(Place).filter_by(chat_id=chat_id)


def db_update_places(message, bot, place_id=None):
    if bot and message.from_user.id != bot.get_me().id:
        if place_id:
            place = session.query(Place).filter_by(id=place_id).first()
            if message.photo and message.photo[0]:
                place.photo_id = message.photo[0].file_id
            elif message.text:
                place.comment = message.text
            elif message.location:
                place.longitude = message.location.longitude
                place.latitude = message.location.latitude
            else:
                return None
        elif message.text:
            place = Place(
                chat_id=message.chat.id,
                name=message.text
            )
            session.add(place)
        else:
            return None
    else:
        return None

    session.commit()
    return place


def db_remove_places(message):
    db_get_places(message.chat.id, 0).delete()
    session.commit()


def db_get_chat(chat_id):
    return session.query(Chat).filter_by(id=chat_id).first()


def db_update_chat(chat_id, step, place_id=None):
    chat = db_get_chat(chat_id)
    if chat:
        chat.step = step
        if place_id:
            chat.place_id = place_id
    else:
        chat = Chat(
            id=chat_id,
            step=step
        )
        session.add(chat)

    session.commit()
    return chat


def get_step(chat_id):
    try:
        step = db_get_chat(chat_id).step
    except AttributeError:
        return None
    return step


def place_exists(message, place_id):
    place = session.query(Place).filter_by(id=place_id).first()
    if place and place.name:
        return True
    return False
