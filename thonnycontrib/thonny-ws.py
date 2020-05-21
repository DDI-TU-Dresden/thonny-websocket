from thonny import get_workbench
import websocket
import threading
from tkinter.simpledialog import askstring


def on_message(ws, message):
    """This method is called if the client received a message.

        Returns:
            None
        """
    print("Message received: " + message)


def on_error(ws, error):
    """This method is called if the client received an error.

        Returns:
            None
        """
    print(error)


def on_close(ws):
    """This method is called after the connection is closed.

        Returns:
            None
        """
    print("Connection closed")


def on_open(ws):
    """This method is called after the connection is opened.

        Returns:
            None
        """
    print("Connection opened")


def run_in_background():
    """This method has to be called in a new thread because it blocks the current thread.

        Returns:
            None
        """
    ws.run_forever()


def send_hello():
    """This method gets called if the ws_send item is called in the tools menu.

        Returns:
            None
        """
    ws.send("hello")


"""
These instructions, besides the thread creation, are executed in global scope if you
want to send messages at a later time. This is because you need the ws object to send
messages. This object cannot be passed on to other functions using the add_command
function that the thonny Workbench class offers. A different solution to still use the
add_command function would be to wrap each method call (Source:
https://stackoverflow.com/questions/52077459/python-pass-extra-arguments-to-callable).
Code in global scope is executed before the load_plugin function call.
"""
server = askstring("Websocket Server", "")
websocket.enableTrace(True)
ws = websocket.WebSocketApp(
    server, on_message=on_message, on_error=on_error, on_close=on_close,
)
ws.on_open = on_open
t = threading.Thread(target=run_in_background)
t.daemon = True
t.start()


def load_plugin():
    """This method gets called if this plugin is in the PYTHONPATH environment variable
       upon starting thonny.

        Returns:
            None
        """
    get_workbench().add_command(
        command_id="ws_send",
        menu_name="tools",
        command_label="Send Hello",
        handler=send_hello,
    )
