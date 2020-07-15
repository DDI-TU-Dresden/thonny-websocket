# Websocket Plugin for the thonny IDE

## Installation

- Install the python dependencies

```bash
pip install -r requirements.txt --user
```

## Start the plugin with thonny

```bash
cd /path/to/thonny/
PYTHONPATH=/path/to/thonny-websocket/ python -m thonny
```

## Usage in thonny

Click on the "Tools" section in the menu at the top of the program. And then select "Add WS Server". You will be asked to input a server address. This server immeadiately echoes the message you send. For testing purposes you can use "wss://echo.websocket.org/". You can click on the "Tools" section in the menu again and select "Send Message" to send a message. After that, you will be asked for the server address and message. You can close a connection by clicking on the "Tools" section in the menu and selecting "Close WS Server connection". Following that, you will be asked for the server address. You can see all the communication on stdout.
