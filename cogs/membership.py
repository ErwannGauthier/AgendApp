from discord.ext import commands
from discord.ext.commands import RoleConverter

from utility.functionUtil import add_role_to_user, remove_role
from utility.groupUtil import is_group_id_in_table_group
from utility.membershipUtil import add_membership_in_db, delete_membership
from utility.userUtil import is_user_in_server_members


class Membership(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["joinGroup", "joingroup", "joinGrp", "joingrp", "join_grp"])
    @commands.guild_only()
    async def join_group(self, ctx, *arg):
        global role
        len_arg = len(arg)

        if len_arg <= 0:
            await ctx.send(">>> Veuillez mentionner le groupe que vous souhaitez rejoindre."
                           "\n\t**Exemple :** `!agenda join_group @groupe`.")
        elif len_arg > 1:
            await ctx.send(">>> Vous ne pouvez pas rejoindre plus d'un groupe à la fois."
                           "\nUtilisez `!agenda join_groups @groupe1 @groupe2 ...` pour cela.")
        else:
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, arg[0])
            except:
                await ctx.send(">>> Veuillez mentionner le groupe lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda join_group @groupe`.")

            is_user_in_server_members(ctx.author, ctx.guild.id)

            if is_group_id_in_table_group(ctx.guild.id, role.id):
                add_membership_in_db(ctx.author.id, ctx.guild.id, role.id)
                await add_role_to_user(ctx.author, role)
                await ctx.send(f">>> ✅ Vous avez rejoint `@{role.name}`.")
            else:
                await ctx.send(">>> ❌ Le groupe n'est pas défini sur le serveur.")

    @commands.command(aliases=["joinGroups", "joingroups", "joinGrps", "joingrps", "join_grps"])
    @commands.guild_only()
    async def join_groups(self, ctx, *arg):
        len_arg = len(arg)

        if len_arg <= 0:
            await ctx.send(">>> Veuillez mentionner les groupes que vous souhaitez rejoindre."
                           "\n\t**Exemple :** `!agenda join_groups @groupe1 @groupe2...`.")
        else:
            roles = []
            args = list(arg)
            for r in args:
                try:
                    converter = RoleConverter()
                    role1 = await converter.convert(ctx, r)
                    roles.append(role1)
                except:
                    await ctx.send(f">>> ❌ Un problème est survenu avec {r}."
                                   "\nProblème récurrent :"
                                   f"\n\tVeuillez mentionner le groupe lors de l'appel de la commande."
                                   f"\n\t\t**Exemple :** `!agenda join_groups @{r}`.")

            if roles:
                rol = ""
                for rl in roles:
                    rol = rol + f"\t• `@{rl.name}`\n"

                message = await ctx.send(f">>> Vous êtes sur le point de rejoindre ces {len(roles)} groupes :"
                                         f"\n{rol}"
                                         f"Confirmez-vous que vous souhaitez les rejoindre ?"
                                         f"\n:white_check_mark: **OUI**\t:x: **NON**")
                await message.add_reaction("✅")
                await message.add_reaction("❌")
                def checkEmoji(react, usr):
                    return ctx.message.author == usr and message.id == react.message.id and (
                            str(react.emoji) == "✅" or str(react.emoji) == "❌")

                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=10, check=checkEmoji)
                    if reaction.emoji == "✅":
                        is_user_in_server_members(ctx.author, ctx.guild.id)

                        for role in roles:
                            if is_group_id_in_table_group(ctx.guild.id, role.id):
                                add_membership_in_db(ctx.author.id, ctx.guild.id, role.id)
                                await add_role_to_user(ctx.author, role)
                                await ctx.send(f">>> ✅ Vous avez rejoint `@{role.name}`.")
                            else:
                                await ctx.send(f">>> ❌ Le groupe (`@{role.name}`) n'est pas défini sur le serveur.")

                    else:
                        await ctx.send(">>> ❌ Vous n'avez pas rejoint les groupes.")
                except:
                    await ctx.send(">>> ❌ Vous n'avez pas rejoint les groupes.")
            else:
                await ctx.send(">>> Vous n'avez mentionné aucun rôle.")

    @commands.command(aliases=["leaveGroup", "leavegroup", "leaveGrp", "leavegrp", "leave_grp"])
    @commands.guild_only()
    async def leave_group(self, ctx, *arg):
        global role
        len_arg = len(arg)

        if len_arg <= 0:
            await ctx.send(">>> Veuillez mentionner le groupe que vous souhaitez rejoindre."
                           "\n\t**Exemple :** `!agenda leave_group @groupe`.")
        elif len_arg > 1:
            await ctx.send(">>> Vous ne pouvez pas quitter plus d'un groupe à la fois."
                           "\nUtilisez `!agenda leave_groups @groupe1 @groupe2 ...` pour cela.")
        else:
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, arg[0])
            except:
                await ctx.send(">>> Veuillez mentionner le rôle lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda leave_group @groupe`.")

            is_user_in_server_members(ctx.author, ctx.guild.id)

            if is_group_id_in_table_group(ctx.guild.id, role.id):
                delete_membership(ctx.author.id, ctx.guild.id, role.id)
                await remove_role(ctx.author, role)
                await ctx.send(f">>> ✅ Vous avez quitté `@{role.name}`.")
            else:
                await ctx.send(">>> ❌ Le groupe n'est pas défini sur le serveur.")

    @commands.command(aliases=["leaveGroups", "leavegroups", "leaveGrps", "leavegrps", "leave_grps"])
    @commands.guild_only()
    async def leave_groups(self, ctx, *arg):
        len_arg = len(arg)

        if len_arg <= 0:
            await ctx.send(">>> Veuillez mentionner les groupes que vous souhaitez quitter."
                           "\n\t**Exemple :** `!agenda leave_groups @groupe1 @groupe2...`.")
        else:
            roles = []
            args = list(arg)
            for r in args:
                try:
                    converter = RoleConverter()
                    role1 = await converter.convert(ctx, r)
                    roles.append(role1)
                except:
                    await ctx.send(f">>> ❌ Un problème est survenu avec {r}."
                                   "\nProblème récurrent :"
                                   f"\n\tVeuillez mentionner le groupe lors de l'appel de la commande."
                                   f"\n\t\t**Exemple :** `!agenda leave_groups @{r}`.")

            if roles:
                rol = ""
                for rl in roles:
                    rol = rol + f"\t• `@{rl.name}`\n"

                message = await ctx.send(f">>> Vous êtes sur le point de quitter ces {len(roles)} groupes :"
                                         f"\n{rol}"
                                         f"Confirmez-vous que vous souhaitez les quitter ?"
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
                            is_user_in_server_members(ctx.author, ctx.guild.id)

                            if is_group_id_in_table_group(ctx.guild.id, role.id):
                                delete_membership(ctx.author.id, ctx.guild.id, role.id)
                                await remove_role(ctx.author, role)
                                await ctx.send(f">>> ✅ Vous avez quitté `@{role.name}`.")
                            else:
                                await ctx.send(">>> ❌ Le groupe n'est pas défini sur le serveur.")
                    else:
                        await ctx.send(">>> ❌ Vous n'avez pas quitté les groupes.")
                except:
                    await ctx.send(">>> ❌ Vous n'avez pas quitté les groupes.")


def setup(client):
    client.add_cog(Membership(client))
