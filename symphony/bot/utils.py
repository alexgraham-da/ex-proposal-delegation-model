from sym_api_client_python.processors.message_formatter import MessageFormatter

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def create_message(msg):
        return MessageFormatter().format_message(msg)

    @staticmethod
    def format_message(msg):
        return msg # f'<messageML>{msg}</messageML>'

