import textwrap
import curses


class Message:
    def __init__(self, text, color=None):
        self.text = text
        if color:
            self.color = color
        else: 
            curses.color_pair(4)

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height
        self.update = True

    def add_message(self, message):
        self.update = True
        lines = textwrap.wrap(message.text, self.width)

        for line in lines:
            if len(self.messages) == self.height:
                del self.messages[0]

            self.messages.append(Message(line, message.color))


