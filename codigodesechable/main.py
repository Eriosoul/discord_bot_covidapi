import datetime
import json, os

import discord
from discord.ext import commands
from lib.covidapi import CovidAPI

def main():
    if os.path.exists('config.json'):
        with open('config.json') as f:
            config_data = json.load(f)
            with open('data.json') as d:
                config_infodata = json.load(d)
    else:
        template = {'prefix!':'!', 'token': ""}
        with open('config.json', 'w') as f:
            json.dump(template, f)
    title = config_infodata["title"]
    description_info = config_infodata["description_info"]
    prefix = config_data["prefix!"]
    token = config_data["token"]
    intent = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intent, description= "Bot moderador")

    @bot.command(name="saludar", help="El bot te saluda")
    async def saludar(ctx):
        await ctx.reply(f'Hola {ctx.author}, ¿Como estas?')

    @bot.command(name='sumar', help='Suma dos numeros')
    async def sumar(ctx, num1:int, num2:int):
        suma = num1+num2
        await ctx.reply(f'El resultado de la suma es : {suma}')

    @bot.command()
    async def nuevoembed(ctx):
        api: CovidAPI = CovidAPI()
        global_data: config_data = api.getAllData()
        await ctx.send(nuevoembed)
        embed = discord.Embed(title=global_data, description=description_info, color=discord.Color.dark_embed())
        embed.add_field(name="Este es mi campo", value="Este es el valor de mi campo", inline=False)
        embed.add_field(name="Este es mi campo", value="Este es el valor de mi campo", inline=True)
        embed.add_field(name="Campo incrustado", value="pincha[aqui](https://google.com)", inline=True)
        embed.set_author(name=ctx.message.author)
        embed.set_thumbnail(
            url="https://muyadictivo.com/wp-content/uploads/2022/07/significado-de-waifu-221-800x500.webp")
        embed.set_image(
            url="https://muyadictivo.com/wp-content/uploads/2022/07/significado-de-waifu-221-800x500.webp")
        embed.set_footer(
            icon_url="https://muyadictivo.com/wp-content/uploads/2022/07/significado-de-waifu-221-800x500.webp"
            ,text="Pie de página del Embed")
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)


    bot.run(token)


if __name__ == '__main__':
    main()