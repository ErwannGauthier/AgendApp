from discord.ext import commands
from discord.ext.commands import RoleConverter

from utility.functionUtil import is_french_date_conform, is_french_date_not_passed, add_year_to_french_date
from utility.groupUtil import is_group_name_in_table_group
from utility.homeworkUtil import add_homework_in_db, list_homeworks, is_homework_already_in_db, is_homework_in_db, \
    delete_homework
from utility.membershipUtil import is_membership_set, is_user_in_membership_table
from utility.subjectUtil import is_subject_in_table_subject, get_subject_id
from utility.userUtil import is_user_in_server_members


class Homework(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["addDevoir", "adddevoir", "addDev", "adddev"])
    @commands.guild_only()
    async def add_devoir(self, ctx, *args):
        global role

        if len(args) < 4:
            await ctx.send(">>> Veuillez saisir correctement la commande."
                           "\n\t**Exemple :** `!agenda add_devoir @groupe matière JJ/MM/AAAA devoirs`.")
        else:
            group = args[0]
            subject = args[1].capitalize()
            date = args[2]
            content = ' '.join(str(c) for c in args[3:])

            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, group)
            except:
                await ctx.send(">>> Veuillez mentionner le rôle lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda add_devoir @groupe matière JJ/MM/AAAA devoirs`.")

            if is_group_name_in_table_group(ctx.guild.id, role.name):
                is_user_in_server_members(ctx.author, ctx.guild.id)
                if is_membership_set(ctx.guild.id, ctx.author.id, role.id):
                    if is_subject_in_table_subject(ctx.guild.id, [subject, subject]):
                        if is_french_date_conform(date):
                            if is_french_date_not_passed(date):
                                date = add_year_to_french_date(date)

                                subject_id = get_subject_id(ctx.guild.id, subject)

                                res, homework = is_homework_already_in_db(ctx.guild.id, subject_id, role.id, date)
                                if res:
                                    message = await ctx.send(
                                        f">>> Il y a déjà des devoirs enregistrés pour ce groupe et cette matière à cette date:"
                                        f"\n\n{homework}"
                                        f"Voulez-vous tout de même ajouter vos devoirs ?"
                                        f"\n:white_check_mark: **OUI**\t:x: **NON**")
                                    await message.add_reaction("✅")
                                    await message.add_reaction("❌")

                                    def checkEmoji(react, usr):
                                        return ctx.message.author == usr and message.id == react.message.id and (
                                                str(react.emoji) == "✅" or str(react.emoji) == "❌")

                                    try:
                                        reaction, user = await self.client.wait_for("reaction_add", timeout=10,
                                                                                    check=checkEmoji)
                                        if reaction.emoji == "❌":
                                            await ctx.send(">>> L'ajout des devoirs a été abandonné.")
                                            return 0
                                    except:
                                        await ctx.send(">>> L'ajout des devoirs a été abandonné.")

                                add_homework_in_db(ctx.guild.id, subject_id, role.id, ctx.author.id, date, content)

                                author = ctx.author.nick
                                if author is None:
                                    author = ctx.author.name

                                await ctx.send(f">>> Les devoirs ont bien été enregistrés."
                                               f"\nGroupe:\t `@{role.name}`"
                                               f"\nMatière:\t`{subject}`"
                                               f"\nDate:\t\t  `{date}`"
                                               f"\nÉcrit par:\t`{author} #{ctx.author.id}`"
                                               f"\nContenu:\t`{content}`")
                            else:
                                await ctx.send(">>> La date est déjà passée.")
                        else:
                            await ctx.send(f">>> La date `{date}` n'est pas conforme."
                                           "\nEssayez `JJ/MM/AA` ou `JJ/MM/AAAA`.")
                    else:
                        await ctx.send(f">>> La matière ou le diminutif `{subject}` n'est pas défini sur le serveur."
                                       "\nUtilisez `!agenda list_matiere` pour consulter la liste des matières.")
                else:
                    await ctx.send(
                        f">>> Veuillez rejoindre le groupe `@{role.name}` pour pouvoir y ajouter des devoirs."
                        f"\n\t**Exemple :** `!agenda join_group @{role.name}`")
            else:
                await ctx.send(f">>> Le groupe `@{role.name}` n'est pas défini sur le serveur."
                               "\nUtilisez `!agenda list_group` pour consulter la liste des groupes.")

    @commands.command(aliases=["delDevoir", "deldevoir", "delDev", "deldev"])
    @commands.guild_only()
    async def del_devoir(self, ctx, *args):
        global role

        if len(args) < 5 or len(args) > 5:
            await ctx.send(">>> Veuillez saisir correctement la commande."
                           "\n\t**Exemple :** `!agenda del_devoir @groupe matière JJ/MM/AAAA id_auteur contenu`."
                           "\n\t\t*L'id_auteur est le nombre après le # de 'Ajouté par:'.*")
        else:
            group = args[0]
            subject = args[1].capitalize()
            date = args[2]
            id_author = args[3]
            content = args[4]

            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, group)
            except:
                await ctx.send(">>> Veuillez mentionner le rôle lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda del_devoir @groupe matière JJ/MM/AAAA`.")

            if is_membership_set(ctx.guild.id, ctx.author.id, role.id):
                if is_french_date_conform(date):

                    is_user_in_server_members(ctx.author, ctx.guild.id)

                    date = add_year_to_french_date(date)

                    subject_id = get_subject_id(ctx.guild.id, subject)

                    res, homework = is_homework_in_db(ctx.guild.id, subject_id, role.id, id_author, date, content)
                    if res:
                        message = await ctx.send(
                            f">>> Vous êtes sur le point de supprimer ces devoirs:"
                            f"\n\n{homework}"
                            f"Etes-vous sûr de vouloir les supprimer ?"
                            f"\n:white_check_mark: **OUI**\t:x: **NON**")
                        await message.add_reaction("✅")
                        await message.add_reaction("❌")

                        def checkEmoji(react, usr):
                            return ctx.message.author == usr and message.id == react.message.id and (
                                    str(react.emoji) == "✅" or str(react.emoji) == "❌")

                        try:
                            reaction, user = await self.client.wait_for("reaction_add", timeout=10,
                                                                        check=checkEmoji)
                            if reaction.emoji == "✅":
                                delete_homework(ctx.guild.id, subject_id, role.id, id_author, date, content)

                                author = ctx.author.nick
                                if author is None:
                                    author = ctx.author.name

                                await ctx.send(
                                    f">>> ✅ Les devoirs ont bien été supprimés par `{author} #{ctx.author.id}`."
                                    f"\n\nGroupe:\t`@{role.name}`"
                                    f"\n\n{homework}")
                            else:
                                await ctx.send(">>> ❌ La suppression des devoirs a été annulée.")

                        except:
                            await ctx.send(">>> ❌ La suppression des devoirs a été annulée.")
                    else:
                        await ctx.send(">>> Aucun devoir ne correspond à votre description:"
                                       f"\n\nGroupe:\t `@{role.name}`"
                                       f"\nMatière:\t`{subject}`"
                                       f"\nDate:\t\t  `{date}`"
                                       f"\nÉcrit par:\t`#{id_author}`"
                                       f"\nContenu:\t`{content}`\n\n"
                                       f"Assurez-vous d'avoir correctement copier/coller les informations.")

                else:
                    await ctx.send(f">>> La date `{date}` n'est pas conforme."
                                   "\nEssayez `JJ/MM/AA` ou `JJ/MM/AAAA`.")
            else:
                await ctx.send(f">>> Veuillez rejoindre le groupe `@{role.name}` pour pouvoir y supprimer des devoirs."
                               f"\n\t**Exemple :** `!agenda join_group @{role.name}`")

    @commands.command(aliases=["Devoir", "dev"])
    @commands.guild_only()
    async def devoir(self, ctx, *args):
        if len(args) > 0:
            await ctx.send(">>> Veuillez saisir correctement la commande."
                           "\n\t**Exemple :** `!agenda devoir`.")
        else:
            is_user_in_server_members(ctx.author, ctx.guild.id)
            if is_user_in_membership_table(ctx.guild.id, ctx.author.id):
                result = list_homeworks(ctx.guild.id, ctx.author.id)

                await ctx.send(result)
            else:
                await ctx.send(">>> Vous n'êtes dans aucun groupe."
                               "\n`!agenda join_group @group` pour rejoindre un groupe.")


def setup(client):
    client.add_cog(Homework(client))
