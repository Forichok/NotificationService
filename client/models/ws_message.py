class WsMessage:

  def __init__(self, msg_type, message, sender, date):
    self.type = msg_type
    self.message = message
    self.sender = sender
    self.date = date
