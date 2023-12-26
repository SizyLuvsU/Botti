import discord, json, time, asyncio
import random, os, string
import requests, aiohttp, datetime
from discord.ext import commands
from discord import Game, Embed, File

token = (
    'MTE2NTk1MzE4NDQ5ODQ1NDY0OA.G80X-G.X34OQLCAWhxuurqvow1bNKAFuUAbvZjR4yX2B4')
prefix = ("!")
RPC = ("made with love by @.h4rmm")

intents = discord.Intents.all()

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
async def ping(ctx):
  await ctx.send(f'***~pong~*** {round (bot.latency *1000)}ms')


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
      print(f"[Pistinkö ees erroria :D]: {e}")
    if r == 404:
      await ctx.send(embed=discord.Embed(title='Sivu on alhaal bro',
                                         description=f'vastas tilalla: {r}'))
    else:
      await ctx.send(
          embed=discord.Embed(title='Sivu on ylhäällä',
                              description=f'vastas tilalla: {r} Ajassa: {t}'))


@bot.command()
async def ddos(ctx):
  await ctx.message.delete()
  messageddos = await ctx.send(
      ":skull_crossbones: Pistit pakettei tulee. Huutista! :skull_crossbones:")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓░░░░░░░░░░░░░░░░░░░░░░ 10%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓░░░░░░░░░░░░░░░░░░░░ 20%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░ 30%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░ 40%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░ 50%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░ 60%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░ 70%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░ 80%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 90%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ 93%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░ 97%")
  await asyncio.sleep(2)
  await messageddos.edit(content="▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%")
  await asyncio.sleep(2)
  await messageddos.edit(
      content=
      ":skull_crossbones: __**Sait se homo offlinee hönö**__ :skull_crossbones:"
  )


bot.run(token)
