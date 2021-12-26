from discord.ext import commands
from discord.ext.commands import RoleConverter

from utility.functionUtil import have_admin_role, arg_into_list, delete_role, verif_dont_starts_and_ends_with_space
from utility.groupUtil import is_group_name_in_table_group, add_group_in_db, get_groups_list, delete_group, \
    add_role_in_db, \
    add_group_to_user_having_role


class Group(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["addGroup", "addgroup",  "addGrp", "addgrp", "add_grp"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def add_group(self, ctx, *arg):
        len_arg = len(arg)
        if len_arg <= 0:
            await ctx.send(">>> Veuillez saisir le nom du groupe que vous souhaitez créer."
                           "\n\t**Exemple :** `!agenda add_group groupe`.")
        elif len_arg > 1:
            await ctx.send(">>> Vous ne pouvez pas ajouter plus d'un groupe à la fois."
                           "\nUtilisez `!agenda add_groups groupe1 groupe2 ...` pour cela.")
        else:
            argument = arg_into_list(arg)
            grp = verif_dont_starts_and_ends_with_space(argument[0])
            if grp != "":
                if not is_group_name_in_table_group(ctx.guild.id, grp):
                    await add_group_in_db(ctx.guild, grp)
                    await ctx.send(f">>> ✅ Le groupe `{grp}` a bien été enregistré.")
                else:
                    await ctx.send(
                        f">>> ❌ Le groupe `{grp}` est déjà défini sur ce serveur."
                        "\nUtilisez `!agenda list_group` pour consulter la liste des groupes.")
            else:
                await ctx.send(">>> ❌ Le groupe doit contenir au moins un caractère.")

    @commands.command(aliases=["addGroups", "addgroups",  "addGrps", "addgrps", "add_grps"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def add_groups(self, ctx, *args):
        len_args = len(args)
        if len_args <= 0:
            await ctx.send(">>> Veuillez saisir au moins un nom de groupe."
                           "\n\t**Exemple :** `!agenda add_groups groupe1 groupe2 groupe3 ...`.")
        else:
            groups = arg_into_list(args)
            group = ""
            for i in range(len(groups)):
                group = group + f"\t• `@{groups[i]}`\n"

            message = await ctx.send(f">>> Vous êtes sur le point d'ajouter ces {len(groups)} groupes :"
                                     f"\n{group}"
                                     f"Confirmez-vous l'ajout de ces groupes au serveur ?"
                                     f"\n:white_check_mark: **OUI**\t:x: **NON**")
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            def checkEmoji(react, usr):
                return ctx.message.author == usr and message.id == react.message.id and (
                        str(react.emoji) == "✅" or str(react.emoji) == "❌")

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=10, check=checkEmoji)
                if reaction.emoji == "✅":
                    for j in range(len(groups)):
                        grp = verif_dont_starts_and_ends_with_space(groups[j]).capitalize()
                        if grp != "":
                            if not is_group_name_in_table_group(ctx.guild.id, grp):
                                await add_group_in_db(ctx.guild, grp)
                                await ctx.send(
                                    f">>> ✅ Le groupe `@{grp}` a bien été enregistré.")
                            else:
                                await ctx.send(
                                    f">>> ❌ Le groupe `@{grp}` est déjà défini sur ce serveur."
                                    "\nUtilisez `!agenda list_group` pour consulter la liste des groupes définis sur ce serveur.")
                        else:
                            await ctx.send(f">>> ❌ Le groupe n°{j+1} doit contenir au moins un caractère.")
                else:
                    await ctx.send(">>> ❌ L'ajout des groupes a été annulé.")
            except:
                await ctx.send(">>> ❌ L'ajout des groupes a été annulé.")

    @commands.command(aliases=["roleIntoGroup", "roleintogroup",  "roleIntoGrp", "roleintogrp", "role_into_grp"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def role_into_group(self, ctx, *arg):
        global role
        len_arg = len(arg)

        if len_arg <= 0:
            await ctx.send(">>> Veuillez mentionner le rôle que vous souhaitez convertir en groupe."
                           "\n**Exemple :** `!agenda role_into_groupe @role`.")
        elif len_arg > 1:
            await ctx.send(">>> Vous ne pouvez pas convertir plus d'un rôle à la fois."
                           "\nUtilisez `!agenda roles_into_groups @role1 @role2 ...` pour cela.")
        else:
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, arg[0])
            except:
                await ctx.send(">>> Veuillez mentionner le rôle lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda role_into_groupe @role`.")

            if not is_group_name_in_table_group(ctx.guild.id, role.name):
                add_role_in_db(ctx.guild.id, role.id, role.name)
                add_group_to_user_having_role(role)
                await ctx.send(f">>> ✅ Le groupe `{role.name}` a bien été enregistré.")
            else:
                await ctx.send(
                    f">>> ❌ Le groupe `{role.name}` est déjà défini sur ce serveur."
                    "\nUtilisez `!agenda list_group` pour consulter la liste des groupes.")

    @commands.command(aliases=["rolesIntoGroups", "rolesintogroups",  "rolesIntoGrps", "rolesintogrps", "roles_into_grps"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def roles_into_groups(self, ctx, *args):
        len_arg = len(args)

        if len_arg <= 0:
            await ctx.send(">>> Veuillez mentionner au moins un rôle que vous souhaitez convertir en groupe."
                           "\n\t**Exemple :** `!agenda roles_into_groupes @role1 @role2`.")
        else:
            roles = []
            rols = ""
            for i in range(len_arg):
                try:
                    converter = RoleConverter()
                    rol = await converter.convert(ctx, args[i])
                    roles.append(rol)
                    rols = rols + f"\t• `@{rol.name}`\n"
                except:
                    await ctx.send(f">>> Veuillez mentionner le rôle lors de l'appel de la commande."
                                   f"\n\t**Exemple :** `!agenda roles_into_groupes @{args[i]}`.")

            message = await ctx.send(f">>> Vous êtes sur le point de convertir ces {len(roles)} rôles :"
                                     f"\n{rols}"
                                     f"Confirmez-vous la conversion de ces rôles en groupes ?"
                                     f"\n:white_check_mark: **OUI**\t:x: **NON**")
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            def checkEmoji(react, usr):
                return ctx.message.author == usr and message.id == react.message.id and (
                        str(react.emoji) == "✅" or str(react.emoji) == "❌")

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=10, check=checkEmoji)
                if reaction.emoji == "✅":
                    for role in roles:
                        if not is_group_name_in_table_group(ctx.guild.id, role.name):
                            add_role_in_db(ctx.guild.id, role.id, role.name)
                            add_group_to_user_having_role(role)
                            await ctx.send(f">>> ✅ Le groupe `{role.name}` a bien été enregistré.")
                        else:
                            await ctx.send(
                                f">>> ❌ Le groupe `{role.name}` est déjà défini sur ce serveur."
                                "\nUtilisez `!agenda list_group` pour consulter la liste des groupes.")
                else:
                    await ctx.send(">>> ❌ La conversion des rôles a été annulée.")
            except:
                await ctx.send(">>> ❌ La conversion des rôles a été annulée.")

    @commands.command(aliases=["delGroup", "delgroup", "delGrp", "delgrp", "del_grp"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def del_group(self, ctx, *arg):
        global role
        if len(arg) != 1:
            await ctx.send(">>> Veuillez saisir correctement la commande."
                           "\n\t**Exemple :** `!agenda del_group @groupe`.")
        else:
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, arg[0])
            except:
                await ctx.send(">>> Veuillez mentionner le rôle lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda del_group @groupe`.")

            if is_group_name_in_table_group(ctx.guild.id, role.name):
                message = await ctx.send(f">>> Vous êtes sur le point de supprimer ce groupe :"
                                         f"\n\t`@{role.name}`\n"
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
                        delete_group(role.id)
                        await delete_role(ctx, role.id)
                        await ctx.send(">>> ✅ Le groupe a bien été supprimé.")
                    else:
                        await ctx.send(">>> ❌ La suppression du groupe a été annulée.")
                except:
                    await ctx.send(">>> ❌ La suppression du groupe a été annulée.")
            else:
                await ctx.send(">>> Le groupe n'est pas défini sur le serveur.")

    @commands.command(aliases=["listGroup", "listgroup", "listGrp", "listgrp", "list_grp"])
    @commands.guild_only()
    async def list_group(self, ctx):
        groups = get_groups_list(ctx.guild.id)

        groups_list = ""
        for group in groups:
            groups_list = groups_list + f"\t• `@{group[0]}`\n"

        if groups_list == "":
            await ctx.send(">>> Ce serveur ne possède aucun groupe.")
        else:
            await ctx.send(f">>> Liste des groupes du serveur :\n{groups_list}")


def setup(client):
    client.add_cog(Group(client))
