import aioimaplib

import email
from email import policy

from typing import AsyncIterator

from django.core.files.base import ContentFile

from mail_extractor.models import Message, Mail, FileMessage
from mail_extractor.utils import format_message


async def get_all_messages():
    async for message in Message.objects.all().aiterator():
        yield message


class MailServiceManager:

    def __init__(self, login: str, password: str, server: str):

        self.login = login
        self.password = password
        self.server = server
        self.message_ids = []
        self.mail = None

    async def connection(self):
        try:
            self.mail = aioimaplib.IMAP4_SSL(self.server)
            await self.mail.wait_hello_from_server()
            await self.mail.login(self.login, self.password)
        except Exception as err:
            # Handle other exceptions or re-raise if you want to propagate
            raise err

    async def logout(self):
        await self.mail.logout()

    async def __aenter__(self) -> "MailServiceManager":

        await self.connection()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        await self.logout()

    async def set_message_ids(self, mail_box: str):

        await self.mail.select(mail_box)
        status, messages = await self.mail.search("ALL")
        if status != "OK":
            await self.mail.logout()
            return {"msg": "Ошибка поиска сообщений"}

        self.message_ids = messages[0].split()
        self.message_ids = [s.decode("ascii") for s in self.message_ids]

    async def get_messages(self) -> AsyncIterator[str]:

        for msg_id in self.message_ids:
            status, msg_data = await self.mail.fetch(msg_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[1], policy=policy.default)
            msg = format_message(msg)
            yield msg


async def message_integration(login, mail_pass, server) -> int:

    mail = await Mail.objects.filter(login=login).afirst()
    async with MailServiceManager(login, mail_pass, server) as mail_manager:
        await mail_manager.set_message_ids("inbox")
        async for msg in mail_manager.get_messages():
            message = Message(
                title=msg.get("title"),
                date_send=msg.get("date_send"),
                date_receiving=msg.get("date_received"),
                text_message=msg.get("content"),
                mail=mail,
            )
            await message.asave()

            message = await Message.objects.filter(pk=message.pk).afirst()

            if message is not None:
                for file in msg["files"]:
                    file_instance = FileMessage(
                        message=message,
                        file=ContentFile(file["payload"], name=file["file_name"]),
                    )
                    await file_instance.asave()
        count_messages = await Message.objects.filter(mail=mail).acount()
        return count_messages