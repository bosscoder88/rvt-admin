import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands import MissingPermissions
from discord import app_commands
from discord.ext.commands.errors import MissingRequiredArgument
import os
import re

## CONSTANTS ##

VERSION = "V1.0 BETA"
ChannelTicket = 803323336603074591
servername = 'Rodston Valley Trains'

## LISTS ##

tickets = []
claimers = []
users = []



intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


## VERSION COMMAND ##
@tree.command(name = "version", description = "Returns bot version number", guild = discord.Object(id=793849239192600576))
async def first_command(interaction):
  await interaction.response.send_message(VERSION)

## QOTD COMMAND ##
@tree.command(name = "postqotd", description = "For the QOTD team to post questions!", guild = discord.Object(id=793849239192600576))
async def second_command(interaction, title: str, question: str):
  poster = interaction.user.nick
  newcontent = f"> **{question}**\n> Answer below please!\n\n<@&848477252743069716>\n**Posted by** {poster}"
  qotdchannel = client.get_channel(1019996772883509349)
  await qotdchannel.create_thread(name = title, content = newcontent, reason = "QOTD")
  await interaction.response.send_message("QOTD Posted. Well Done! :)")

## SEND COMMAND ##
@tree.command(name = "sendmessage", description = "For staff members to message members of the server", guild = discord.Object(id=793849239192600576))
async def third_command(interaction, user: discord.Member, message: str, confidential: bool):
  if confidential == True:
      sender = interaction.user.nick
      newcontent = f"> <:RVT_Black:992366190926233610> This is a confidential message from **{sender}** from the RVT Management Team.\n> If you have received this DM in error, please contact the RVT Directors as soon as possible.\n||```{message}```||"
    
  else:
      sender = interaction.user.nick
      newcontent = f"> <:RVT_Black:992366190926233610> This is a message from **{sender}** from the RVT Management Team:\n```{message}```"
    
  await user.send(content = newcontent)
  await interaction.response.send_message("Message sent")

## SAY COMMAND ##
@tree.command(name="saychannel", description = "Send a message through the bot to a certain channel", guild = discord.Object(id=793849239192600576))
async def fourth_command(interaction, channel: discord.TextChannel, message: str, showauthor:bool=True, publish:bool=False):
  if showauthor == True:
    newcontent = f"> <:RVT_Black:992366190926233610> **This is a message from {interaction.user.nick}**\n\n```{message}```"
  else:
    newcontent = f"{message}"
  sentMessage = await channel.send(content = newcontent)

  if publish == True:
    try:
      await sentMessage.publish()
      await interaction.response.send_message("Message sent :thumbsup:")
    except:
      await interaction.response.send_message("Message failed to publish. Check the channel you sent it to is an announcement channel")
  else:
    await interaction.response.send_message("Message sent :thumbsup:")


## CAPS CHECKER ##
@client.event
async def on_message(ctx):
  caps = "[A-Z]"
  lower = "[a-z]"
  
  tcaps = re.findall(caps, ctx.content)
  tlower = re.findall(lower, ctx.content)
  if len(tcaps)+len(tlower) == 0:
    pass
  elif len(tlower) == 0 and len(tcaps) >= 6:
    warnMessage = await ctx.channel.send(f"> ‼️ Too many caps, **{ctx.author.mention}**!")
    await warnMessage.delete(delay = 5)
  elif len(tcaps)/len(tlower) >= 0.65 and len(tcaps) >= 6:
    warnMessage = await ctx.channel.send(f"> ‼️ Too many caps, **{ctx.author.mention}**!")
    await warnMessage.delete(delay = 5)


@client.event
async def on_ready():
  await tree.sync(guild=discord.Object(id=793849239192600576))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="bosscoder"))
  print("Ready")


client.run("MTAxMDQ2OTMyNzU1NzkwNjQ2OA.GWbIvF.zoCeiiO0J2Bqxjt6d9yWouAtEAkl40MJPivK7E")