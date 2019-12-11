class WsMessage:

  def __init__(self, msg_type, message, sender, date):
    self.type = msg_type
    self.message = message
    self.sender = sender
    self.date = date

  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)