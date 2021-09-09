import aiohttp, configparser, discord, os, json, datetime, requests, random
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
config_path = os.getenv('path to direcotry of', 'config.ini') 
excitegif_path = os.getenv(' path to direcotry of', 'excitegif.json') 
streamer_path = os.getenv('path to direcotry of', 'streamers.json') 
config = configparser.ConfigParser() 
config.read(config_path) 
streamer_api = config['twitch']['streamer_api'] 
game_api = config['twitch']['game_api'] 
client_id = config['twitch']['clientid'] 
follows_api = config['twitch']['follows_api']

headers= {'Client-ID': client_id} 
Secret = 'twitch secret' 
AutURL ='https://id.twitch.tv/oauth2/token'

class DiscordClient(discord.Client):
    async def on_ready(self):
class Streamer():
    def __init__(self, streamer, frequency, message, channel):
        self.streamer = streamer
        self.went_live = 0
        self.live_last_tick = False
        self.message = ""
        self.message = message
        self.channel = channel
        self.job = sched.add_job(self.process_live_check, 'interval', seconds=80,misfire_grace_time=5400)
        self.job = sched.add_job(self.check_follow_increment, 'interval', seconds=80,misfire_grace_time=5400)
        self.embed = discord.Embed(title=f"https://twitch.tv/{self.streamer}")
        self.first_time_in_code = 0
        self.original_total_follows = 0
        
    async def process_live_check(self):
        role = ''
        if (live_data := await self.is_live()) is not None:
            if not self.live_last_tick:
                now = int(datetime.datetime.now().strftime('%s'))
                if ((now - self.went_live) > 120):
                    self.went_live = int(datetime.datetime.strptime(live_data[0]['started_at'], "%Y-%m-%dT%H:%M:%SZ").strftime('%s'))
                    self.live_last_tick = True
                    game_data = await self.get_game_data(live_data[0]['game_id'])
                    self.embed.add_field(name='Title', inline=False, value=live_data[0]['title'])
                    self.embed.add_field(name='Current Viewership', inline=False, value = live_data[0]['viewer_count'])
                    self.embed.add_field(name='Category', inline=False, value=game_data['name'])
                    role = addRoleToMessage(game_data['name'], self.message)
                    if(role != "None"):
                        self.message = role + self.message
                    self.embed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{self.streamer}-1920x1080.jpg")
                    channel = discord_client.get_channel(int(self.channel))
                    await channel.send(content=self.message, embed=self.embed)
                    self.embed.clear_fields()
                    self.message = self.message.replace(role,'',1);
                else:
                    self.live_last_tick = True
            else:
                self.live_last_tick = True
        else:
            self.live_last_tick = False
    async def is_live(self):
        AutParams = {'client_id': client_id, 'client_secret': Secret, 'grant_type': 'client_credentials'}
        AutCall = requests.post(url=AutURL, params=AutParams)
        data1 = AutCall.json()
        access_token = data1['access_token']
        Headers = {'Client-ID': client_id, 'Authorization': 'Bearer ' + access_token}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{streamer_api}{self.streamer}", headers=Headers) as r:
                live_data = await r.json()
                if len(live_data['data']) > 0:
                    return live_data['data']
                else:
                    return None
    async def get_game_data(self, game_id):
        AutParams = {'client_id': client_id, 'client_secret': Secret, 'grant_type': 'client_credentials'}
        AutCall = requests.post(url=AutURL, params=AutParams)
        data1 = AutCall.json()
        access_token = data1['access_token']
        Headers = {'Client-ID': client_id, 'Authorization': 'Bearer ' + access_token}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{streamer_api}{self.streamer}", headers=Headers) as r:
                game_data = await r.json()
            if len(game_data['data']) > 0:
                return {
                'name': game_data['data'][0]['game_name'],
                'art': game_data['data'][0]['thumbnail_url'].format(width="170", height="226")
                }
            else:
                return None
            
    async def check_follow_increment(self):
        if (live_data := await self.follow_count()) is not None:
            excitegiflist = []
            with open(excitegif_path, 'r') as f:
                excitegifjson = json.load(f)
                for excitegif in excitegifjson:
                    excitegiflist += [excitegif['url']]
                random.shuffle(excitegiflist)
                randomexcitegif = excitegiflist[0]
            self.embed.add_field(name='Title', inline=False, value=f"OH! {self.streamer} Just Got A Follow! Much Excite!")
            self.embed.set_image(url=randomexcitegif)
            channel = discord_client.get_channel(int(self.channel))
            await channel.send(content="Look at who just got a follow!", embed=self.embed)
            self.embed.clear_fields()
    async def follow_count(self):
        AutParams = {'client_id': client_id, 'client_secret': Secret, 'grant_type': 'client_credentials'}
        AutCall = requests.post(url=AutURL, params=AutParams)
        data1 = AutCall.json()
        access_token = data1['access_token']
        Headers = {'Client-ID': client_id, 'Authorization': 'Bearer ' + access_token}
        async with aiohttp.ClientSession() as session:
           async with session.get(url=f"{streamer_api}{self.streamer}", headers=Headers) as r:
                live_data = await r.json()
                if len(live_data['data']) > 0:
                   user_id = live_data['data'][0]['user_id']
                   user_login = live_data['data'][0]['user_login']
                   async with session.get(url=f"{follows_api}{user_id}", headers=Headers) as s:
                        follows_data = await s.json()
                        if(self.first_time_in_code == 0):
                            self.first_time_in_code += 1
                            self.original_total_follows = follows_data['total']
                        total_follows = follows_data['total']
                        if(total_follows > self.original_total_follows):
                            self.original_total_follows += 1
                            return live_data['data']
                        else:
                           return None
def add_streamer(twitch_username, message, channel):
    if '@here' in message or '@everyone' in message:
        return None
    else:
        sched.pause()
        streamer = {
        "twitch_name": twitch_username,
        "frequency": 5,
        "active": True,
        "message": message,
        "announce_channel": channel
        }
        Streamer(streamer['twitch_name'], streamer['frequency'], streamer['message'], streamer['announce_channel'])
        with open(sstreamer_pathtreamer_path, 'w') as f:
            streamers = json.load(f)
            streamers.append(streamer)
            f.write(json.dump(streamers))
def addRoleToMessage(game_data, message):
    if("Game_Category" in game_data or "Uncharted" in game_data):
        role = ''
        role = '<@&DiscordRoleId> '
        return role
    else:
        role = ''
        return role
def set_announce_channel(server, channel):
    if not server in config:
        config[server] = {}
    config[server]['announce_channel'] = channel
    with open(config_path, 'w') as configfile:
        config.write(configfile) 
discord_client = DiscordClient() 
sched = AsyncIOScheduler() 
with open(streamer_path, 'r') as f:
    streamers = json.load(f)
    for streamer in streamers:
        if streamer['active']:
            streamer_obj = Streamer(streamer['twitch_name'], streamer['frequency'], streamer['message'], streamer['announce_channel']) 
sched.start() 
discord_client.run(config['discord']['token'])
