from discord.ext import commands

from utility.functionUtil import init_agendadmin_role, verif_agendadmin_exist, verif_not_group_role
from utility.groupUtil import is_group_id_in_table_group, update_group_name
from utility.membershipUtil import add_membership_in_db, delete_membership
from utility.serverUtil import add_server, delete_server
from utility.userUtil import is_user_in_server_members


class Event_reference(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        role_admin = await init_agendadmin_role(guild)
        add_server(guild, role_admin)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        delete_server(guild.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await verif_agendadmin_exist(role)
        verif_not_group_role(role)

    @commands.Cog.listener()
    async def on_guild_role_update(self, old, new):
        if old.name != new.name:
            if is_group_id_in_table_group(old.guild.id, old.id):
                update_group_name(new.id, new.name)

    @commands.Cog.listener()
    async def on_member_update(self, old, new):
        is_user_in_server_members(new, new.guild.id)

        if old.roles != new.roles:
            for o_role in old.roles:
                if o_role not in new.roles:
                    if is_group_id_in_table_group(o_role.guild.id, o_role.id):
                        delete_membership(new.id, new.guild.id, o_role.id)

            for n_role in new.roles:
                if n_role not in old.roles:
                    if is_group_id_in_table_group(n_role.guild.id, n_role.id):
                        add_membership_in_db(new.id, new.guild.id, n_role.id)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.client.user.display_name} is ready.")


def setup(client):
    client.add_cog(Event_reference(client))
