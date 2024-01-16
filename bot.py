import discord, json, time, asyncio
import random, os, string
import requests, aiohttp, datetime
import socket
import re
from mcstatus import JavaServer
from discord.ext import commands
from discord import Game, Embed, File
from ping3 import ping, verbose_ping
from keep_alive import keep_alive

keep_alive()

token = (
    'Your token here')
prefix = ("!")
RPC = ("Noutaja made this one ;)")

intents = discord.Intents.all()
intents.invites = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
  print("Im alive bitch")
  await bot.change_presence(status=discord.Status.online,
                            activity=discord.Game(RPC))


@bot.event
async def on_command_error(error, ctx):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("En haluukkaa toimia :D! Huutista!")


@bot.command()
async def botping(ctx):
  await ctx.send(f'*** Pingi *** {round (bot.latency *1000)}ms')


@bot.command()
async def geoip(ctx, *, ipaddr: str = '9.9.9.9'):
  r = requests.get(f'http://ip-api.com/json/{ipaddr}?fields=192511')

  geo = r.json()
  em = discord.Embed()
  fields = [
      {
          'name': 'IP',
          'value': geo['query']
      },
      {
          'name': 'Country',
          'value': geo['country']
      },
      {
          'name': 'City',
          'value': geo['city']
      },
      {
          'name': 'ISP',
          'value': geo['isp']
      },
      {
          'name': 'Latitute',
          'value': geo['lat']
      },
      {
          'name': 'Longitude',
          'value': geo['lon']
      },
      {
          'name': 'Org',
          'value': geo['org']
      },
      {
          'name': 'Region',
          'value': geo['region']
      },
      {
          'name': 'Status',
          'value': geo['status']
      },
      {
          'name': 'Proxy?',
          'value': geo['proxy']
      },
  ]
  for field in fields:
    if field['value']:
      em.set_footer(text='\u200b')
      em.timestamp = datetime.datetime.utcnow()
      em.add_field(name=field['name'], value=field['value'], inline=True)
  return await ctx.send(embed=em)


@bot.command()
async def pingweb(ctx, website=None):
  if website is None:
    await ctx.send(
        "Vitu taukki laita se sivun osote jos haluut pingaa [tarvii http/https alkuun] :D"
    )
  else:
    try:
      r = requests.get(website).status_code
      t = requests.get(website).elapsed.total_seconds()
    except Exception as e:
      await ctx.send(embed=discord.Embed(
          title='Ei se toimi noi bro laita linkkinä se :D'))
    if r == 404:
      await ctx.send(embed=discord.Embed(title='Sivu on alhaal bro',
                                         description=f'vastas tilalla: {r}'))
    else:
      await ctx.send(
          embed=discord.Embed(title='Sivu on ylhäällä',
                              description=f'vastas tilalla: {r} Ajassa: {t}'))


@bot.command(name="invite_info")
async def invite_info(ctx, invite_code):
  try:
    invite = await bot.fetch_invite(invite_code)
    await ctx.send(
        f"Invite Info:\n"
        f"Invite koodi: {invite.code}\n"
        f"Servu: {invite.guild.name}\n"
        f"Kanava: {invite.channel.name}\n"
        f"Invaaja: {invite.inviter.name if invite.inviter else 'Joku neekeri vrm en tiiä en löytäny'}\n"
        f"Käytöt: {invite.uses}\n"
        f"Max käyttö kerrat: {invite.max_uses}\n"
        f"Umpeutuu: {invite.expires_at}")
  except discord.errors.NotFound:
    await ctx.send("Invitee ei löytyny :D")
  except discord.errors.HTTPException:
    await ctx.send("Heitti jonku vitu http errori :D")


@bot.command(name='clear')
async def clear(ctx, amount=5):
  # Check if the user has an admin role
  if any(role.name == 'clear' for role in ctx.author.roles):
    # Purge messages
    await ctx.channel.purge(limit=amount + 1
                            )  # +1 to include the command message
    await ctx.send(f'Poistettu {amount} viestii :D')
  else:
    await ctx.send("Ei taida neekerillä olla oikeuksia tämmösee xD")


@bot.event
async def on_message(message):
  if message.author.bot:
    return  # Ignore messages from other bots

  # Check if the message contains a specific word or phrase
  if 'neekeri' in message.content.lower():
    # Respond to the specific word or phrase
    await message.channel.send(
        f'Moro, {message.author.mention}! Kuulin juttuu et oot neekeri. Huutista neekerille :D',
        tts=True)

  await bot.process_commands(message)  # Ensure commands still work


@bot.command(name="mcresolve")
async def resolve_minecraft_ip(ctx, server_address):
  try:
    ip_address = socket.gethostbyname(server_address)
    response = f"Servun : {server_address} ip on : {ip_address}"
  except socket.error as e:
    response = f"Heitin errori xD: {e}"

  await ctx.send(response)


# Define playing status command
@bot.command(aliases=["cfx", "fivem", "server"])
async def find(ctx, cfx):
  if "https://cfx.re/join/" in cfx:
    cfxcode = cfx[20:]
  elif "http://cfx.re/join/" in cfx:
    cfxcode = cfx[19:]
  elif "cfx.re/join/" in cfx:
    cfxcode = cfx[12:]
  elif "https://servers.fivem.net/servers/detail/" in cfx:
    cfxcode = cfx[41:]
  elif "http://servers.fivem.net/servers/detail/" in cfx:
    cfxcode = cfx[40:]
  else:
    cfxcode = cfx

  r = requests.get(
      f"https://servers-frontend.fivem.net/api/servers/single/{cfxcode}",
      headers={
          "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
      })
  if r.text == '{"error": "404 Not Found"}':
    findnieznalembed = discord.Embed(
        title=":x:  Server not found",
        colour=discord.Colour(0xf40552),
        description=f"The server you specified wasn't found by the bot!")
    findnieznalembed.set_thumbnail(
        url=
        "https://images-ext-1.discordapp.net/external/jPuVkQCmDg9zmBk6xAanj4_l1gJmtnXTBVZ8XPtQxaw/https/freepngimg.com/save/37007-angry-emoji/512x536"
    )
    findnieznalembed.set_footer(
        text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=findnieznalembed)
  else:
    r = r.json()
    ep = r['EndPoint']
    hn = r['Data']['hostname']
    onlc = r['Data']['clients']
    maxc = r['Data']['sv_maxclients']
    lc = r['Data']['vars']['locale']
    svl = r['Data']['vars']['sv_lan']
    votes = r['Data']['upvotePower']
    iv = r['Data']['iconVersion']
    ip = r['Data']['connectEndPoints'][0]
    size = len(ip)
    ipbez = ip[:size - 6]
    rip = requests.get(f"https://db-ip.com/demo/home.php?s={ipbez}")
    rip = rip.json()
    country = rip['demoInfo']['countryCode']
    city = rip['demoInfo']['city']
    isp = rip['demoInfo']['isp']
    org = rip['demoInfo']['organization']
    build = ""
    bld = requests.get(
        f"https://servers-frontend.fivem.net/api/servers/single/{cfxcode}",
        headers={
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
        })
    if "sv_enforceGameBuild" in bld.text:
      bld = bld.json()
      build = bld['Data']['vars']['sv_enforceGameBuild']
    else:
      build = "1604"

    findznalembed = discord.Embed(
        title=":white_check_mark:  Server found",
        colour=discord.Colour(0xf40552),
        description=
        f"\nCode: `{ep}`\nHostname: `{hn}`\nSlots: `{onlc}/{maxc}`\nBuild: `{build}`\nLocale: `{lc}`\nsv_lan: `{svl}`\nVotes: `{votes}`\n\n\n/info.json: [Click here](http://{ip}/info.json)\n/players.json [Click here](http://{ip}/players.json)\n/dynamic.json [Click here](http://{ip}/dynamic.json)\n\n\nIP: `{ip}`\nCountry: `{country}`\nCity: `{city}`\nISP: `{isp}`\nOrganization: `{org}`\n"
    )
    findznalembed.set_thumbnail(
        url=f"https://servers-live.fivem.net/servers/icon/{ep}/{iv}.png")
    findznalembed.set_footer(text="PY-Finder",
                             icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=findznalembed)


bot.run(token)
