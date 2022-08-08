import threading

from sqlalchemy import Column, String, UnicodeText

from database import BASE, SESSION


class Ocr(BASE):
    __tablename__ = "ocr"
    chat_id = Column(String(14), primary_key=True)
    chat_name = Column(UnicodeText)

    def __init__(self, chat_id, chat_name=None):
        self.chat_id = chat_id
        self.chat_name = chat_name


Ocr.__table__.create(checkfirst=True)

CHATS_LOCK = threading.RLock()
CHATS_ID = set()


def add_user_ocr(chat_id, chat_name=None):
    with CHATS_LOCK:
        chat = SESSION.query(Ocr).get(str(chat_id))
        if not chat:
            chat = Ocr(str(chat_id), chat_name)
        else:
            chat.chat_name = chat_name

        SESSION.add(chat)
        SESSION.commit()


def rem_user_ocr(chat_id):
    with CHATS_LOCK:
        chat = SESSION.query(Ocr).get(str(chat_id))
        if chat:
            SESSION.delete(chat)
        SESSION.commit()


def list_ocr_user():
    global CHAT_ID
    try:
        CHAT_ID = {int(x.chat_id) for x in SESSION.query(Ocr).all()}
        return CHAT_ID
    finally:
        SESSION.close()
