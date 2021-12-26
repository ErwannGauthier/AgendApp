from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def HELP(self, ctx, *arg):
        try:
            len_arg = len(arg)
            if len_arg > 1:
                ctx.send(">>> Veuillez saisir correctement la commande."
                         "\n\t**Exemple :** `!agenda HELP catégorie`.")
            else:
                if len_arg <= 0:
                    arg = "help"
                else:
                    arg = arg[0].lower()
                category = ["group", "help", "homework", "membership", "membership_admin", "other", "subject"]
                if arg not in category:
                    await ctx.send(">>> Veuillez saisir une catégorie existante."
                                   "\nSaisissez `!agenda HELP` pour avoir la liste des catégories disponibles.")
                else:
                    file = open(f"utility/help/{arg}.txt", "r", encoding="utf-8")
                    text = file.read()
                    file.close()
                    await ctx.send(text)
        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(Help(client))
