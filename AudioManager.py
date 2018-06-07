import asyncio
import aiohttp
import json
from AudioNode import AudioNode
from AudioPlayer import AudioPlayer
from discord import Guild, VoiceChannel

class AudioManager:
    """
    Class of the AudioManager section.
    This is main class and controls all stuff like joining channels, leaving channels, and launching nodes.
    """
    def __init__(self, bot, nodes=[], shards=1):
        self.nodes = {}
        self.players = {}
        self.shards = shards
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.bot.loop.create_task(self._spawn_nodes(nodes)) 

    def _create_player(self, guild: Guild, node: AudioNode):
        player = self.players.get(guild.id)
        if not player:
            player = AudioPlayer(guild, self, node)

        return player
    
    async def connect(self, channel: VoiceChannel, host: str):
        await self.bot.ws.send(json.dumps({
            "op": 4,
            "shard": self.shards,
            "d": {
                "guild_id": channel.guild.id,
                "channel_id": channel.id,
                "self_mute": False,
                "self_deaf": False
            }
        }))
        if not self.nodes.get(host):
            raise Exception("No node with host: {} found.".format(host))
        self._create_player(channel.guild, self.nodes.get(host))
        
    async def _spawn_nodes(self, nodes: []):
        for i in range(len(nodes)):
            node = AudioNode(self, self.shards, nodes[i]["host"], nodes[i]["password"], nodes[i]["port"])
            await node.launch(self.bot)
            self.nodes[node.host] = node