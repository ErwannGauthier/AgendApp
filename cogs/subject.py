from discord.ext import commands

from utility.functionUtil import have_admin_role, arg_into_list
from utility.subjectUtil import is_subject_in_table_subject, add_subject_in_db, get_subjects_list, delete_subject


class Subject(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["addMatiere", "addmatiere", "addMat", "addmat", "add_mat"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def add_matiere(self, ctx, *arg):
        len_arg = len(arg)
        if len_arg <= 0:
            await ctx.send(">>> Veuillez saisir correctement la commande."
                           "\n\t**Exemple :** `!agenda add_matiere Mathématiques Maths`.")
        elif len_arg == 1:
            await ctx.send(">>> Veuillez ajouter un diminutif en deuxième argument."
                           "\n\t**Exemple :** `!agenda add_matiere Mathématiques Maths`.")
        elif len_arg > 2:
            await ctx.send(">>> Vous ne pouvez pas ajouter plus d'une matière à la fois."
                           "\nUtilisez `!agenda add_matieres matiere1 diminutif1 matiere2 diminutif2...` pour cela.")
        elif len(arg[0]) < len(arg[1]):
            await ctx.send(">>> Le nom de la matière ne peut pas être plus court que son diminutif.")
        else:
            argument = arg_into_list(arg)
            if not is_subject_in_table_subject(ctx.guild.id, argument):
                add_subject_in_db(ctx.guild.id, argument)
                await ctx.send(f">>> ✅ La matière `{argument[0]}` (`{argument[1]}`) a bien été enregistrée.")
            else:
                await ctx.send(
                    f">>> ❌ La matière `{argument[0]}` et/ou son diminutif `{argument[1]}` sont déjà définis sur ce serveur."
                    "\nUtilisez `!agenda list_matiere` pour consulter la liste des matières.")

    @commands.command(aliases=["addMatieres", "addmatieres", "addMats", "addmats", "add_mats"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def add_matieres(self, ctx, *args):
        len_args = len(args)
        if len_args <= 0:
            await ctx.send(">>> Veuillez saisir correctement la commande."
                           "\n\t**Exemple :** `!agenda add_matieres Mathématiques Maths Français Fr`.")
        elif len_args % 2 != 0:
            await ctx.send(">>> Chaque matière doit avoir un diminutif (et vis versa)."
                           "\n\t**Exemple :** `!agenda add_matieres Mathématiques Maths Français Fr`.")
        else:
            subjects = arg_into_list(args)
            subj = ""
            i = 0
            while i < len(subjects) - 1:
                subj = subj + f"\t• `{subjects[i]}` (`{subjects[i + 1]}`)\n"
                i += 2
            message = await ctx.send(f">>> Vous êtes sur le point d'ajouter ces {int(len(subjects) / 2)} matières :"
                                     f"\n{subj}"
                                     f"Confirmez-vous l'ajout de ces matières au serveur ?"
                                     f"\n:white_check_mark: **OUI**\t:x: **NON**")
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            def checkEmoji(react, usr):
                return ctx.message.author == usr and message.id == react.message.id and (
                        str(react.emoji) == "✅" or str(react.emoji) == "❌")

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=10, check=checkEmoji)
                if reaction.emoji == "✅":
                    j = 0
                    while j < len(subjects) - 1:
                        subj_couple = [subjects[j], subjects[j + 1]]
                        if len(subj_couple[0]) > len(subj_couple[1]):
                            if not is_subject_in_table_subject(ctx.guild.id, subj_couple):
                                add_subject_in_db(ctx.guild.id, subj_couple)
                                await ctx.send(
                                    f">>> ✅ La matière `{subj_couple[0]}` (`{subj_couple[1]}`) a bien été enregistrée.")
                            else:
                                await ctx.send(
                                    f">>> ❌ La matière `{subj_couple[0]}` et/ou son diminutif `{subj_couple[1]}` sont déjà définis sur ce serveur."
                                    "\nUtilisez `!agenda list_matiere` pour consulter la liste des matières définies sur ce serveur.")
                        else:
                            await ctx.send(
                                f">>> ❌ Le nom de la matière `{subj_couple[0]}` ne peut pas être plus court que son diminutif `{subj_couple[1]}`.")
                        j += 2
                else:
                    await ctx.send(">>> ❌ L'ajout des matières a été annulé.")
            except:
                await ctx.send(">>> ❌ L'ajout des matières a été annulé.")

    @commands.command(aliases=["delMatiere", "delmatiere", "delMat", "delmat", "del_mat"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def del_matiere(self, ctx, *arg):

        if len(arg) != 1:
            await ctx.send(">>> Veuillez saisir correctement la commande."
                           "\n\t**Exemple :** `!agenda del_matiere Maths`.")

        subj = arg[0].capitalize()

        if is_subject_in_table_subject(ctx.guild.id, [subj, subj]):
            message = await ctx.send(f">>> Vous êtes sur le point de supprimer cette matière :"
                                     f"\n\t`{subj}`\n"
                                     f"Confirmez-vous sa suppression ?"
                                     f"\n:white_check_mark: **OUI**\t:x: **NON**")
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            def checkEmoji(react, usr):
                return ctx.message.author == usr and message.id == react.message.id and (
                        str(react.emoji) == "✅" or str(react.emoji) == "❌")

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=10, check=checkEmoji)
                if reaction.emoji == "✅":
                    delete_subject(ctx.guild.id, subj)
                    await ctx.send(">>> ✅ La matière a bien été supprimée.")
                else:
                    await ctx.send(">>> ❌ La suppression de la matière a été annulée.")
            except:
                await ctx.send(">>> ❌ La suppression de la matière a été annulée.")
        else:
            await ctx.send(">>> La matière ou le diminutif n'est pas défini sur le serveur.")

    @commands.command(aliases=["listMatiere", "listmatiere", "listMat", "listmat", "list_mat"])
    @commands.guild_only()
    async def list_matiere(self, ctx):
        subjects = get_subjects_list(ctx.guild.id)

        subjectsList = ""
        for subj in subjects:
            subjectsList = subjectsList + f"\t• `{subj[0]}` (`{subj[1]}`)\n"

        if subjectsList == "":
            await ctx.send(">>> Ce serveur ne possède aucune matière.")
        else:
            await ctx.send(f">>> Liste des matières du serveur :\n{subjectsList}")


def setup(client):
    client.add_cog(Subject(client))
