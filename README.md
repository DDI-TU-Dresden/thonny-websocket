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

You will be prompted to provide a server name. This is done via a dialog. For testing purposes you can use "ws://echo.websocket.org/". This server immeadiately echoes the message you send. To send a message select the "tools" section in the menu and then select "Send Hello". You can see all the communication on stdout.
