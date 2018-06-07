from AudioNode import AudioNode
from AudioManager import AudioManager
from Events import TrackStart
from discord import Guild
import pyee

class AudioPlayer:
    """
    Class of AudioPlayer.
    This class has many uses.
    It can play music, skip music, pause music, resume music, seek music, and much more.
    """
    def __init__(self, guild: Guild, manager: AudioManager, node: AudioNode):
        self._guild = guild
        self._manager = manager,
        self._node = node
        self.playing = False
        self.queue = []
        self._emitter = pyee.EventEmitter

    async def add_to_queue(self, track):
        self.queue.append(track)

    async def play(self, track):
        await self._node._send(op="play", guildId=self._guild.id, track=track)
        self._emitter.emit("track_start", TrackStart(self, track))