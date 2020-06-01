from thonny import get_workbench
import websocket
from threading import Thread
from tkinter.simpledialog import askstring


def on_message(ws, message):
    """This method is called if the client received a message.
    
    :param ws: WebSocketApp object

    :param message: message object represented as string

    Returns:
        None
    """
    print("Message from " + ws.url + " received: " + message)


def on_error(ws, error):
    """This method is called if the client received an error.
    
    :param ws: WebSocketApp object

    :param error: error object

    Returns:
        None
    """
    print("Error from " + ws.url + " received: " + error)


def on_close(ws):
    """This method is called after the connection is closed.
    
    :param ws: WebSocketApp object

    Returns:
        None
    """
    print("Connection closed to server: " + ws.url)


def on_open(ws):
    """This method is called after the connection is opened.
    
    :param ws: WebSocketApp object

    Returns:
        None
    """
    print("Connection opened to server: " + ws.url)


def run_in_background():
    """This method has to be called in a new thread because it blocks the current
    thread. It will listen for messages from the latest added WebSocketApp object.

    Returns:
        None
    """
    wsList = Singleton.getInstance().get_wsList()
    ws = wsList[len(wsList) - 1]
    ws.run_forever()


class Singleton:
    """This Singleton class is needed because the list of WebSocketApp objects is shared.

    __instance: The current instance of this class.
        """

    __instance = None

    @staticmethod
    def getInstance():
        """This is an unmodified Singleton.getInstance() method. It will create a new
        instance only once.
        
        Returns:
            Nested Singleton object with the list of WebSocketApp objects
        """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """This is an unmodified Singleton constructor. The singleton instance will
        contain an empty list.
        """
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.wsList = []
            Singleton.__instance = self

    def get_wsList(self):
        """This method gets the list of WebSocketApp objects.

        Returns:
            list of WebSocketApp objects
        """
        return self.wsList

    def add_ws(self, ws):
        """This method adds a WebSocketApp object to the list.

        :param ws: WebSocketApp object

        Returns:
            None
        """
        self.wsList.append(ws)

    def remove_ws(self, server_address):
        """This method removes a WebSocketApp object with a given server address from
        the list.

        :param server_address: server address represented as a string

        Returns:
            None
        """
        for ws in self.wsList:
            if ws.url == server_address:
                self.wsList.remove(ws)
                ws.close()
                return

    def send_message(self, server_address, message):
        """This method sends a message to a server with the given server address and
        message.

        :param server_address: server address represented as a string

        :param message: message represented as a string

        Returns:
            None
        """
        for ws in self.wsList:
            if ws.url == server_address:
                ws.send(message)
                print("Sent " + message + " to " + ws.url)
                return
        print(
            "Message can't be sent to "
            + server_address
            + " as there is no established connection."
        )


def add_ws_server():
    """This method gets called if the "Add WS Server" command is clicked in the "tools"
    menu. It will create a WebSocketApp object with a given server_address and then get
    the Singleton instance. After that, it will create a new thread and call the
    "run_in_background" method.

        Returns:
            None
        """
    server_address = askstring("Websocket", "Which server would you like to add?")
    ws = websocket.WebSocketApp(
        server_address, on_message=on_message, on_error=on_error, on_close=on_close,
    )
    ws.on_open = on_open
    Singleton.getInstance().add_ws(ws)
    t = Thread(target=run_in_background)
    t.daemon = True
    t.start()


def close_ws_server():
    """This method gets called if the "Close WS Server connection" command is clicked
    in the "tools" menu. It will get the Singleton instance and call the remove_ws
    method with the given server address.
    
        Returns:
            None
        """
    server_address = askstring("Websocket", "Which server connection should be closed?")
    Singleton.getInstance().remove_ws(server_address)


def send_message():
    """This method gets called if the "Send Message" command is clicked
    in the "tools" menu. It will get the Singleton instance and call the send_message
    method with the given server address and message.
    
        Returns:
            None
        """
    server_address = askstring("Websocket", "Which server would you like to message?")
    message = askstring("Message", "What is your message?")
    Singleton.getInstance().send_message(server_address, message)


def load_plugin():
    """This method gets called if this plugin is in the PYTHONPATH environment variable
       upon starting thonny. It will add the needed commands to the thonny workbench.

        Returns:
            None
        """
    # This method enables DEBUG messages
    websocket.enableTrace(True)
    get_workbench().add_command(
        command_id="ws_add",
        menu_name="tools",
        command_label="Add WS Server",
        handler=add_ws_server,
    )
    get_workbench().add_command(
        command_id="ws_remove",
        menu_name="tools",
        command_label="Close WS Server connection",
        handler=close_ws_server,
    )
    get_workbench().add_command(
        command_id="ws_remove",
        menu_name="tools",
        command_label="Send Message",
        handler=send_message,
    )
