import datetime
import discord
from discord.ext import commands
from lib.covidapi import CovidAPI


class MyBot(commands.Bot):
    def __init__(self, prefix: str, token: str, intent: discord.Intents):
        super().__init__(command_prefix=prefix, intents=intent, description="Bot moderador")
        self.add_commands()
        self.api: CovidAPI = CovidAPI()

    def add_commands(self):
        @self.command(name="saludar", help="El bot te saluda")
        async def saludar(ctx):
            await ctx.reply(f'Hola {ctx.author}, ¿Cómo estás?')

        @self.command(name='sumar', help='Suma dos numeros')
        async def sumar(ctx, num1: int, num2: int):
            suma: int = num1+num2
            await ctx.reply(f'El resultado de la suma es : {suma}')

        @self.command(name='pais', help='Debera introducir el comando + el pais')
        async def nuevoembed(ctx, nombrepais: str = None, fecha: int = None):
            try:
                if nombrepais is None:
                    raise Exception("Debes proporcionar un nombre de país")
                else:
                    global_data: dict = self.api.get_country_info(nombrepais)
                    descipcion: str = ",".join([global_data.iso3, global_data.iso2])
                    embed = discord.Embed(title=f"{global_data.country} ({descipcion})",
                                          description=f"Información sobre el COVID-19 en {global_data.country}",
                                          color=discord.Color.dark_embed())

                    embed.add_field(name="Nº de casos", value=global_data.cases, inline=True)
                    embed.add_field(name="Nº muertos", value=global_data.deaths, inline=True)
                    embed.add_field(name="Nº de recuperados", value=global_data.deaths, inline=True)
                    embed.add_field(name="Continente", value=global_data.continent, inline=False)

                    # embed.set_author(name=ctx.message.author)
                    embed.set_thumbnail(url=global_data.flag)
                    embed.set_image(url=global_data.flag)
                    embed.set_footer(icon_url=global_data.flag, text="Ultima actualización")
                    embed.timestamp = get_time(global_data.updated, fecha or 0)
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="Error al obtener la información del país", color=discord.Color.dark_red())
                embed.add_field(name="Error",
                                value=f"No se ha podido encontrar el país {nombrepais}. Vuelve a intentarlo. Error: {e}")
                await ctx.send(embed=embed)

        def get_time(updated: int, fecha: int):
            timestamp: datetime = updated / 1000
            date: datetime = datetime.datetime.fromtimestamp(timestamp)
            return date + datetime.timedelta(days=fecha)