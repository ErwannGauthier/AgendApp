from discord.ext import commands
from discord.ext.commands import RoleConverter, MemberConverter

from utility.functionUtil import have_admin_role, add_role_to_user, remove_role
from utility.groupUtil import is_group_id_in_table_group
from utility.membershipUtil import add_membership_in_db, delete_membership
from utility.userUtil import is_user_in_server_members


class Membership_admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["amtg", "addMemberToGroup", "addmembertogroup", "addMembToGrp", "addmembtogrp"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def add_member_to_group(self, ctx, *args):
        global member, role
        len_args = len(args)

        if len_args < 2:
            await ctx.send(">>> Veuillez mentionner le groupe et le membre que vous souhaitez ajouter."
                           "\n\t**Exemple :** `!agenda add_member_to_group @groupe @user`.")
        elif len_args > 2:
            await ctx.send(">>> Vous ne pouvez pas ajouter plus d'un membre à la fois."
                           "\nUtilisez `!agenda add_members_to_group @groupe @user1 @user2 ...` pour cela.")
        else:
            run = True
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, args[0])

                converter = MemberConverter()
                member = await converter.convert(ctx, args[1])
            except:
                run = False
                await ctx.send(">>> Veuillez mentionner le groupe puis le membre lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda add_member_to_group @group @user`.")

            if run:
                is_user_in_server_members(ctx.author, ctx.guild.id)
                is_user_in_server_members(member, ctx.guild.id)

                if is_group_id_in_table_group(ctx.guild.id, role.id):
                    add_membership_in_db(member.id, ctx.guild.id, role.id)
                    await add_role_to_user(member, role)
                    await ctx.send(f">>> ✅ `@{member.name}` a rejoint `@{role.name}`.")
                else:
                    await ctx.send(">>> ❌ Le groupe n'est pas défini sur le serveur.")

    @commands.command(aliases=["amstg", "addMembersToGroup", "addmemberstogroup", "addMembsToGrp", "addmembstogrp"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def add_members_to_group(self, ctx, *args):
        global role
        len_args = len(args)

        if len_args < 2:
            await ctx.send(">>> Veuillez mentionner le groupe et le membre que vous souhaitez ajouter."
                           "\n\t**Exemple :** `!agenda add_member_to_group @groupe @user`.")
        else:
            run = True
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, args[0])
            except:
                run = False
                await ctx.send(">>> Veuillez mentionner le groupe puis les membres lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda add_members_to_group @group @user1 @user2...`.")

            if run:
                if is_group_id_in_table_group(ctx.guild.id, role.id):
                    arg_members = args[1:]
                    members = []

                    for m in arg_members:
                        try:
                            converter = MemberConverter()
                            mem = await converter.convert(ctx, m)
                            members.append(mem)
                        except:
                            await ctx.send(f">>> ❌ Un problème est survenu avec {m}."
                                           "\nProblème récurrent :"
                                           f"\n\tVeuillez mentionner le membre lors de l'appel de la commande."
                                           f"\n\t\t**Exemple :** `!agenda add_members_to_group @group @{m}`.")

                    if members:
                        for member in members:
                            is_user_in_server_members(ctx.author, ctx.guild.id)
                            is_user_in_server_members(member, ctx.guild.id)

                            add_membership_in_db(member.id, ctx.guild.id, role.id)
                            await add_role_to_user(member, role)
                            await ctx.send(f">>> ✅ `@{member.name}` a rejoint `@{role.name}`.")

                else:
                    await ctx.send(">>> ❌ Le groupe n'est pas défini sur le serveur.")

    @commands.command(aliases=["rmfg", "removeMemberFromGroup", "removememberfromgroup", "rmMembFromGrp", "rmmembfromgrp"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def remove_member_from_group(self, ctx, *args):
        global member, role
        len_args = len(args)

        if len_args < 2:
            await ctx.send(">>> Veuillez mentionner le groupe et le membre que vous souhaitez ajouter."
                           "\n\t**Exemple :** `!agenda remove_member_from_group @groupe @user`.")
        elif len_args > 2:
            await ctx.send(">>> Vous ne pouvez pas supprimer plus d'un membre à la fois."
                           "\nUtilisez `!agenda remove_members_from_group @groupe @user1 @user2 ...` pour cela.")
        else:
            run = True
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, args[0])

                converter = MemberConverter()
                member = await converter.convert(ctx, args[1])
            except:
                run = False
                await ctx.send(">>> Veuillez mentionner le groupe puis le membre lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda remove_member_from_group @group @user`.")

            if run:
                is_user_in_server_members(ctx.author, ctx.guild.id)
                is_user_in_server_members(member, ctx.guild.id)

                if is_group_id_in_table_group(ctx.guild.id, role.id):
                    delete_membership(member.id, ctx.guild.id, role.id)
                    await remove_role(member, role)
                    await ctx.send(f">>> ✅ `@{member.name}` a quitté `@{role.name}`.")
                else:
                    await ctx.send(">>> ❌ Le groupe n'est pas défini sur le serveur.")

    @commands.command(aliases=["rmsfg", "removeMembersFromGroup", "removemembersfromgroup", "rmMembsFromGrp", "rmmembsfromgrp"])
    @commands.guild_only()
    @commands.check(have_admin_role)
    async def remove_members_from_group(self, ctx, *args):
        global role
        len_args = len(args)

        if len_args < 2:
            await ctx.send(">>> Veuillez mentionner le groupe et le membre que vous souhaitez ajouter."
                           "\n\t**Exemple :** `!agenda remove_members_from_group @group @user1 @user2...`.")
        else:
            run = True
            try:
                converter = RoleConverter()
                role = await converter.convert(ctx, args[0])
            except:
                run = False
                await ctx.send(">>> Veuillez mentionner le groupe puis le membre lors de l'appel de la commande."
                               "\n\t**Exemple :** `!agenda remove_members_from_group @group @user1 @user2...`.")

            if run:
                if is_group_id_in_table_group(ctx.guild.id, role.id):
                    arg_members = args[1:]
                    members = []

                    for m in arg_members:
                        try:
                            converter = MemberConverter()
                            mem = await converter.convert(ctx, m)
                            members.append(mem)
                        except:
                            await ctx.send(f">>> ❌ Un problème est survenu avec {m}."
                                           "\nProblème récurrent :"
                                           f"\n\tVeuillez mentionner le membre lors de l'appel de la commande."
                                           f"\n\t\t**Exemple :** `!agenda remove_members_from_group @group @{m}`.")

                    if members:
                        for member in members:
                            is_user_in_server_members(ctx.author, ctx.guild.id)
                            is_user_in_server_members(member, ctx.guild.id)

                            delete_membership(member.id, ctx.guild.id, role.id)
                            await remove_role(member, role)
                            await ctx.send(f">>> ✅ `@{member.name}` a quitté `@{role.name}`.")

                else:
                    await ctx.send(">>> ❌ Le groupe n'est pas défini sur le serveur.")


def setup(client):
    client.add_cog(Membership_admin(client))
