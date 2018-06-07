import websockets
import asyncio
import logging
import json
from Events import TrackStart, TrackEnd, QueueConcluded
from AudioManager import AudioManager

class AudioNodeException(Exception):
    """
    An exception raised for when a error occurres.
    """


class TrackNotFound(Exception):
    """
    An exception raised for when a track was not found.
    """

class AudioNode:
    def __init__(self, manager: AudioManager, shards, host=None, password=None, port=None):
        if host is None or port is None or password is None:
            raise AudioNodeException("No password, host, and/or port was provided.")
        self.stats = []
        self.manager = manager
        self.bot = None,
        self.shards = shards
        self.ready = False
        self.ws = None
        self.host = host
        self.password = port
        self.port = port
        self.stats = None

    def __str__(self):
        return f"""
<AudioNode class>
A lavalink node class for the lavalink manager.
Shards: {self.shards}
Host: {self.host}
Port: {self.port}"""

    async def _handle_message(self):
        if self.ws is not None:
            data = json.loads(await self.ws.recv())

            if data["op"] == "playerUpdate":
                player = self.manager.players.get(int(data["guildId"]))
                player.state["timestamp"] = data["state"]["time"]
                player.state["position"] = data["state"]["position"]

            if data["op"] == "stats":
                del data["op"]
                self.stats = data

            if data["op"] == "event":
                player = self.manager.players.get(int(data["guildId"]))
                if data["type"] == "TrackEndEvent":
                    if player: 
                        player._emitter.emit("track_end", TrackEnd(player, data["track"]))

    def node_header(self, bot):
        return {
            "Authorization": self.password,
            "Num-Shards": self.shards,
            "User-Id": bot.user.id
        }

    async def launch(self, bot):
        self.bot = bot
        self.ws = await websockets.connect("ws://{}:{}".format(self.host, self.port), extra_headers=self.node_header(bot))
        logging.log(logging.INFO, "[AudioNode] Node #{}'s connnection has been established.".format(len(self.manager.nodes)))

    async def _send(self, **data):
        if self.ws:
            await self.ws.send(json.dumps(data))
