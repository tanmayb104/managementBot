

import discord
from discord.ext import commands
from botpass import *
import os
import smtplib

EMAIL_ADDRESS = userid
EMAIL_PASSWORD = userpass

client = discord.Client()

d=dict()
emails=dict()
delete=dict()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    
    id = client.get_guild(729892665390268467)


    # Counts the number of messages by each member
    if "BOT" in str(message.author.name):
        pass
    elif "GitHub" in str(message.author.name):
        pass
    else:

        if message.channel.name in d:
            if message.author.name in d[message.channel.name]:
                d[message.channel.name][message.author.name]+=1
            else:
                d[message.channel.name][message.author.name]=1

            delete[message.channel.name].append(message.id)

        else:
            d[message.channel.name]=dict()
            d[message.channel.name][message.author.name]=1

            delete[message.channel.name]=list()
            delete[message.channel.name].append(message.id)

        if message.channel.name not in emails:
            emails[message.channel.name]=dict()



    if message.content == "!users":                 # To find number of users in the channel 
        await message.channel.send(f"# of Members: {id.member_count}")

    elif message.content == "!msgcnt":              # To find number of messages sent by each users
        for i in d[message.channel.name]:
            await message.channel.send(f"{i}: {d[message.channel.name][i]}")

    elif message.content == "!rstcnt":             # To reset the count of messages of each user in a channel
        d[message.channel.name]=dict()

    # Just for checking
    elif message.content == "!delete":
        #print(delete)
        messages=await message.channel.fetch_message(delete[message.channel.name].pop(0))
        #print(messages)
        #a=delete[message.channel.name].pop(0)
        #print(a)
        #await message.delete(a)
        #await message.channel.delete_messages(messages)
        await messages.delete(delay=None)



    elif str(message.content)[:5] == "!del ":      # To delete the number of messages specified
        await message.channel.purge(limit=min(100,int(str(message.content[5:]))))
        await message.channel.send(f"{min(100,int(str(message.content[5:])))} messages Deleted")


    elif str(message.content[:6]) == "!email":       # Add the emails of the members
        email_add=message.content[6:]
        if email_add not in emails:
            emails[message.channel.name][message.author.name]=email_add.strip()


    elif message.content == "!help":                 # To show all the possible options available with the bot
        embed = discord.Embed(title="Help on BOT", description="Some useful commands")
        embed.add_field(name="!users",value="Returns the number of users in the channel")
        embed.add_field(name="!email <email id>",value="Sends an email when a pull request is made")
        embed.add_field(name="!del <int>",value="Deletes the specified number of messages")
        embed.add_field(name="!msgcnt",value="Returns the number of messages sent by each user")
        embed.add_field(name="!rstcnt",value="Resets the number of messages of each user to Zero")
        await message.channel.send(content=None, embed=embed)


    elif "GitHub" in str(message.author.name):      #To send emails when a Github Pull request is made

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = "An update was made to the git repository"
            body = ""

            for i in message.embeds:
                body+=i.title+"\n\n"
                body+=i.description+"\n\n\n\n"

            msg = f"Subject: {subject}\n\n{body}"

            email_ids=emails[message.channel.name].values()
            for i in email_ids:
                smtp.sendmail(EMAIL_ADDRESS,i,msg)



@client.event
async def on_member_remove(member):

    # To remove the member from the messages count and their email from the email
    var_a=str(member.name)
    for i in list(d.keys()):
        if var_a in d[i]:
            d[i].pop(var_a)

    for i in list(emails.keys()):
        if var_a in emails[i]:
            emails[i].pop(var_a)
        


client.run(token)