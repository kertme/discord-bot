from keep_alive import keep_alive
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# client = discord.Client()
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(
    brief='Move user, !bring nickname, role or all',
    description=
    'Move user to your channel, you can specify a nickname, role or all ')
async def bring(ctx, name=None):
    owner_flag = await bot.is_owner(ctx.author)
    connected_flag = ctx.author.voice
    if connected_flag:
        if owner_flag:
            if name:
                members = ctx.guild.members
                connected_members = [x for x in members if x.voice != None]

                if name == 'all':
                    if len(connected_members) == 0:
                        await ctx.send('There is no one on the voice channels')
                    else:
                        for connected_member in connected_members:
                            await connected_member.move_to(
                                connected_flag.channel)

                elif ctx.message.role_mentions:
                    wanted_roles = [x for x in ctx.message.role_mentions]
                    connected_members = [
                        x for x in connected_members
                        if any(item in wanted_roles for item in x.roles)
                    ]
                    for connected_member in connected_members:
                        await connected_member.move_to(connected_flag.channel)

                else:
                    matches = [
                        x for x in connected_members
                        if (name.lower() in x.name.lower()) and x
                    ]
                    if len(matches) == 0:
                        await ctx.send('Username not found on voice channels')
                    elif len(matches) > 1:
                        await ctx.send(
                            f'There are {len(matches)}, try to be more specific.'
                        )
                    else:
                        await matches[0].move_to(connected_flag.channel)
            else:
                await ctx.send('Please specify the user, ex: !bring nickname')
        else:
            await ctx.send(
                f'{ctx.author.mention} You do not have permission for that command.'
            )
    else:
        await ctx.send(
            f'{ctx.author.mention} You should be in a voice channel for this command'
        )


@bot.command()
async def derank(ctx, name):
    owner_flag = await bot.is_owner(ctx.author)
    if owner_flag:
        members = ctx.guild.members
        matches = [x for x in members if (name.lower() in x.name.lower())]
        if len(matches) == 0:
            await ctx.send('Username not found on the discord')
        elif len(matches) > 1:
            print(matches)
            await ctx.send(
                f'There are {len(matches)}, try to be more specific.')
        else:
            user = matches[0]
            owner_flag = await bot.is_owner(user)
            if owner_flag:
                ctx.send('You can not use derank command on Admins')
            else:
                temp_roles = user.roles
                temp_roles.remove(ctx.guild.default_role)
                await user.remove_roles(*temp_roles)
                await user.add_roles(
                    discord.utils.get(ctx.author.guild.roles, name='Derank'))
    else:
        await ctx.send(
            f'{ctx.author.mention} You do not have permission for that command.'
        )


@bot.command()
async def mute(ctx, name=None):
    owner_flag = await bot.is_owner(ctx.author)
    if owner_flag:
        if name:
            if name == 'c':
                if ctx.author.voice:
                    perms = ctx.author.voice.channel.overwrites_for(
                        ctx.guild.default_role)
                    perms.speak = False
                    connected_members = ctx.author.voice.channel.members
                    for i in connected_members:
                        if i is not ctx.author:
                            await i.edit(mute=True)

                    await ctx.author.voice.channel.set_permissions(
                        ctx.guild.default_role, overwrite=perms)
                else:
                    await ctx.send(
                        'You need to be in a voice channel for channel mute command.'
                    )
            else:
                members = ctx.guild.members
                connected_members = [x for x in members if x.voice != None]
                matches = [
                    x for x in connected_members
                    if (name.lower() in x.name.lower())
                ]
                if len(matches) == 0:
                    await ctx.send('Username not found on voice channels')
                elif len(matches) > 1:
                    await ctx.send(
                        f'There are {len(matches)}, try to be more specific.')
                else:
                    await matches[0].edit(mute=True)
        else:
            await ctx.send('Please specify the user, ex: !mute nickname')
    else:
        await ctx.send(
            f'{ctx.author.mention} You do not have permission for that command.'
        )


@bot.command()
@commands.is_owner()
async def unmute(ctx, name):
    if name:
        if name == 'c':
            if ctx.author.voice:
                perms = ctx.author.voice.channel.overwrites_for(
                    ctx.guild.default_role)
                perms.speak = True
                connected_members = ctx.author.voice.channel.members
                for i in connected_members:
                    await i.edit(mute=False)
                await ctx.author.voice.channel.set_permissions(
                    ctx.guild.default_role, overwrite=perms)
        else:
            members = ctx.guild.members
            connected_members = [x for x in members if x.voice != None]
            matches = [
                x for x in connected_members
                if (name.lower() in x.name.lower()) and x
            ]
            if len(matches) == 0:
                await ctx.send('Username not found on voice channels')
            elif len(matches) > 1:
                await ctx.send(
                    f'There are {len(matches)}, try to be more specific.')
            else:
                await matches[0].edit(mute=False)
    else:
        await ctx.send('Please specify the user, ex: !mute nickname')


@bot.command()
async def count(ctx):
    voice_channel_list = ctx.guild.voice_channels

    nobody_flag = True
    for voice_channel in voice_channel_list:
        if len(voice_channel.members) != 0:
            nobody_flag = False

            members_names = []
            for members in voice_channel.members:
                if members.nick == None:
                    members_names.append(members.name)
                else:
                    members_names.append(members.nick)
            members_names = '\n'.join(members_names)
            embed = discord.Embed(title="{} member(s) in {}".format(
                len(voice_channel.members), voice_channel.name),
                                  description=members_names,
                                  color=discord.Color.blue())
            await ctx.send(embed=embed)

    if nobody_flag:
        await ctx.send('There is no one in voice channels.')


@bot.command()
async def clear(ctx, amount=None):
    # msg = await ctx.channel.history().flatten()
    if amount:
        await ctx.channel.purge(limit=int(amount) + 1)
    else:
        await ctx.channel.purge()
    # for i in messages:
    # print(i.content)


@bot.command(name='eval')
@commands.is_owner()
async def _eval(ctx, *, code):
    print(code)
    """A bad example of an eval command"""
    await ctx.send(eval(code))


@bot.command()
async def snap(ctx, *, arg=None):
    a = ctx.message.attachments
    embed = discord.Embed()
    if a:
        url = a[0].url
        embed.set_image(url=url)
        #await ctx.send('testing', embed=embed)

    delay = 3
    text = arg

    if arg:
        try:
            msg = arg.split(" ")
            if msg[-1].isnumeric():
                delay = float(msg[-1])
                text = ' '.join(msg[:-1])
        except:
            print('some error occured.')
    if a:
        await ctx.send(text, embed=embed, delete_after=delay)
    else:
        await ctx.send(text, delete_after=delay)
    await ctx.message.delete()


@bot.command()
async def repeat(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


@bot.command()
async def hello(ctx):
    mention = ctx.author.mention
    response = f"Hey {mention}, hello!"
    await ctx.send(response)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.run(os.getenv('TOKEN'))

keep_alive()
