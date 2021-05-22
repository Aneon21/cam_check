import discord
import asyncio
from discord import channel
from discord import message
from discord import guild

from discord.utils import get
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='?')
wanted_channel_id = None

@client.event
async def on_ready():
    print('I am online and ready')
    Check.start()




@client.command(name='hello')
async def Greet(ctx):
    await ctx.send('Hi')




@client.command(name='join')
async def join(ctx):

    global wanted_channel_id

    for channel in ctx.guild.channels:
        if channel.name == 'YOUTUBE STUDY ROOM 4':
            wanted_channel_id = channel.id
            print(wanted_channel_id)
    try:
        roles = ctx.message.author.roles   
        flag = 0
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            voice = get(client.voice_clients, guild=ctx.guild)

            for role in roles:
                if str(role) == 'CCAdmin':
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()
                    flag = 1
                    break
                else:
                    print(role)
            if flag == 0:
                await ctx.send('You do not have the permission to use this command')
        else:
            await ctx.send('You are not connected to any voice channel')
    except: 
        print('Possibly restart required')



@client.command(name='leave')
async def join(ctx):
    try:
        roles = ctx.message.author.roles
        flag = 0
        for role in roles:
                if str(role) == 'CCAdmin':
                    await ctx.voice_client.disconnect()
                    flag = 1
                    break
                else:
                    print(role)
        if flag == 0:
            await ctx.send('You do not have the permission to use this command')
    except:
        print('Possibly restart required')


@tasks.loop(seconds = 90)
async def Check():
    try:
        channel = get(client.voice_clients).channel
        members = channel.members
        for member in members:
            if str(member)!= 'Cam Check#4539' and str(member) != 'Enrico Vincente#0782':
                if member.voice.self_video:
                    print(f"{member} has cam on")
                else:
                    print(f"{member} has cam off")
                    moveChannel = client.get_channel(wanted_channel_id)
                    await member.move_to(moveChannel)
                    await member.guild.system_channel.send(f'{member.mention}, you were removed from Youtube **CAM ONLY** room for not having your camera on. Please keep your camera on to stay in the room.')

    except:
        print('Not in any voice channel')



@client.event
async def on_voice_state_update(member, before, after):

    ID = None
    try:
        ID = get(client.voice_clients).channel.id
    except:
        print("Skipped error")
    
    if before.channel is None and after.channel is not None:           
        if ID is not None and after.channel.id == ID:
            if str(member) != 'Cam Check#4539':
                if str(member) != 'Enrico Vincente#0782':
                    await member.guild.system_channel.send(f'{member.mention}, you have entered a **CAM ONLY** channel! Please make sure you have your camera turned on.')
    elif before.channel is not None and after.channel is not None:
        if(ID is not None and after.channel.id == ID):
            if(before.channel.id != ID):
                if str(member) != 'Cam Check#4539':
                    if str(member) != 'Enrico Vincente#0782':
                        await member.guild.system_channel.send(f'{member.mention}, you have entered a **CAM ONLY** channel! Please make sure you have your camera turned on.')


client.run('ODQ0OTQ2NTIwNzIwNTM5Njk4.YKZzxA.Y7DhwIu8w80Uac8ujsMM_kkSjgE')