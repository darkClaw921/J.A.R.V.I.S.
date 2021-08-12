from simple_bot import Bot  # базовый класс бота из файла simple_bot
from calendar_bot import GoogleCalendar
from vk_api.longpoll import VkLongPoll, VkEventType  # использование VkLongPoll и VkEventType


class LongPollBot(Bot):
    """
    Бот, прослушивающий в бесконечном цикле входящие сообщения и способный отвечать на некоторые из них
    Бот отвечает на строго заданные сообщения
    """

    # длительное подключение
    long_poll = None

    def __init__(self):
        """
        Иинициализация бота
        """
        super().__init__()
        self.long_poll = VkLongPoll(self.vk_session)

    def run_long_poll(self):
        """
        Запуск бота
        """
        for event in self.long_poll.listen():

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                
                attachmentMessage = event.attachments
        
                if bool(attachmentMessage) == False: # это просто сообщение 
                    
                    message = event.text.lower()
                    if message == 'привет' or message == "здравствуй":

                    # ответ отправляется в личные сообщения пользователя (если сообщение из личного чата)
                        if event.from_user:
                            self.send_message(receiver_user_id=event.user_id, message_text="И тебе привет")

                    # ответ отпрвляется в беседу (если сообщение было получено в общем чате)
                        elif event.from_chat:
                            self.send_message(receiver_user_id=event.chat_id, message_text="Всем привет")
               
                    if message == "че делаешь?" or message == "че делаешь" or message == "что делаешь?" or  message == "что делаешь":
                        calendar = GoogleCalendar()
                        textEvent = calendar.get_events_list()
                        
                        if event.from_user:
                            self.send_message(receiver_user_id=event.user_id, 
                                message_text=f"(J.A.R.V.I.S.) Расписание господина Герасимова на сегодня:\n{textEvent}")
                try:
                    if attachmentMessage['attach1_kind'] == 'audiomsg':
                        self.send_message(
                            receiver_user_id=event.user_id, 
                            message_text='(J.A.R.V.I.S.) Господин Герасимов ограничил прием аудио сообщений \n\n Сообщение не доставлено')
                except:
                    continue
            # если пришло новое сообщение - происходит проверка текста сообщения


                 