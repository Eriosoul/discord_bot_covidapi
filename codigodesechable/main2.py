import datetime
import json, os
import discord

from discord.ext import commands
from lib.covidapi import CovidAPI

def main():
    if os.path.exists('config.json'):
        with open('config.json') as f:
            config_data = json.load(f)
    else:
        template = {'prefix!':'!', 'token': ""}
        with open('config.json', 'w') as f:
            json.dump(template, f)

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

    @bot.command(name='pais', help='Debera introducir el comando + el pais')
    async def nuevoembed(ctx, nombrepais: str):
        try:
            api: CovidAPI = CovidAPI()
            global_data = api.get_country_info(nombrepais)
            timestamp = global_data.updated / 1000
            fecha = datetime.datetime.fromtimestamp(timestamp)
            descipcion = ",".join([global_data.iso3, global_data.iso2])
            embed = discord.Embed(title=global_data.country, description=descipcion,
                                  color=discord.Color.dark_embed())

            embed.add_field(name="Nº de casos", value=global_data.cases, inline=True)
            embed.add_field(name="Nº muertos", value=global_data.deaths, inline=True)
            embed.add_field(name="Nº de recuperados", value=global_data.deaths, inline=True)
            embed.add_field(name="Continente", value=global_data.continent, inline=False)

            embed.set_author(name=ctx.message.author)
            embed.set_thumbnail(url=global_data.flag)
            embed.set_image(url=global_data.flag)
            embed.set_footer(icon_url=global_data.flag, text="Ultima actualización")
            embed.timestamp = fecha
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error al obtener la información del país", color=discord.Color.dark_red())
            embed.add_field(name="Error",
                            value=f"No se ha podido encontrar el país {nombrepais}. Vuelve a intentarlo. Error: {e}")
            await ctx.send(embed=embed)


    bot.run(token)


if __name__ == '__main__':
    main()