import discord
from discord import app_commands
from utility import is_allowed
from config import OWNERS

def setup(tree, client):
    @tree.command(
        name="datamining_string",
        description="Simulate a String Occurences Log APP message"
    )
    async def datamining_string(interaction: discord.Interaction):
        if not is_allowed(interaction, [], OWNERS):
            await interaction.response.send_message("You cannot use this command.", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="String Occurences Changed - b46f6897feaa759f0dc30140335723dcf8660f49",
            color=discord.Color.from_str("#676767")
        )
        embed.set_author(name="String Occurences Log APP")
        
        diff_text = "```diff\nDiff\n1  + \n   GUILD_AUTOMOD_ACTIONS_USER_DISABLE_COMMUNICATION_DIS\n   PLAY_HELPER: 3 (0 -> 3)\n```"
        embed.add_field(name="Notice Types", value=diff_text, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @tree.command(
        name="datamining_commit",
        description="Simulate a Discord-Datamining commit comment message"
    )
    async def datamining_commit(interaction: discord.Interaction):
        if not is_allowed(interaction, [], OWNERS):
            await interaction.response.send_message("You cannot use this command.", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="[Discord-Datamining/Discord-Datamining] New comment on commit 55c98b5",
            color=discord.Color.from_str("#676767")
        )
        embed.set_author(name="Dziurwa14")
        
        diff_text = "```diff\nDiff\n1  + VIDEO_BACKGROUND_UNAVAILABLE\n```"
        embed.add_field(name="Notice Types", value=diff_text, inline=False)
        embed.set_footer(text="20/06/2026 02:20")
        
        await interaction.response.send_message(embed=embed)

    @tree.command(
        name="datamining_rollout",
        description="Simulate a Guild Experiment Rollout Changed message"
    )
    async def datamining_rollout(interaction: discord.Interaction):
        if not is_allowed(interaction, [], OWNERS):
            await interaction.response.send_message("You cannot use this command.", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="Guild Experiment Rollout Changed",
            description="2026-03_guild_official_messages (3747270261)",
            color=discord.Color.from_str("#676767")
        )
        
        overrides_text = "`Guild ID in` `1339367154960564326, 1379947376764256378, 1489752596544753727, 1509228247320232169`\n"
        overrides_text += "```python\n1  (100%) Treatment 1: 0 - 10000\n```"
        embed.add_field(name="Overrides Formatted", value=overrides_text, inline=False)
        
        populations_text = "```python\n1  (100%) None: 0 - 10000\n```"
        embed.add_field(name="Populations", value=populations_text, inline=False)
        
        await interaction.response.send_message(content="<@&Rollouts>", embed=embed)
