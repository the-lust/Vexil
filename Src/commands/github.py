import discord
import requests
from discord import app_commands
import blacklist
from utility import is_jailed

# if the value starts with "$", then the following should be interpreted as a key for this
# if a key does not exist, https://github.com/Unnamed-org123/<key> gets checked.
# aliases & links in this directory are assumed to be correct and won't be checked.
# value must end with "/{owner}/repo" if it's not an alias -> no branches
REPOS = {
    "vexil": "https://github.com/Unnamed-org123/Vexil",
    "bot": "https://github.com/Unnamed-org123/Vexil",
    "website": "https://github.com/Unnamed-org123/Web",
    "tests": "https://github.com/Unnamed-org123/Tests",
    "tutorials": "https://github.com/Unnamed-org123/Tutorials",
    "zed": "https://github.com/Unnamed-org123/Zed",
    "vscode": "https://github.com/Unnamed-org123/VSCode",
    "sublime": "https://github.com/Unnamed-org123/SublimeText",

    # alias
    "vsc": "$vscode",
    "sublimetext": "$sublime",
}

async def repo_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name="Vexil (Compiler)", value="vexil"),
        app_commands.Choice(name="Vexil Bot", value="bot"),
        app_commands.Choice(name="Vexil Website", value="website"),
        app_commands.Choice(name="Vexil (Tests)", value="tests"),
        app_commands.Choice(name="Tutorials", value="tutorials"),
        app_commands.Choice(name="Zed (Extension)", value="zed"),
        app_commands.Choice(name="VS Code (Extension)", value="vscode"),
        app_commands.Choice(name="Sublime Text (Extension)", value="sublime")
    ]



def setup(tree, client):
    @tree.command(
        name="repo",
        description="Get a link to a Vexil repository"
    )
    @app_commands.autocomplete(repository=repo_autocomplete)
    async def repo(
        interaction: discord.Interaction,
        repository: str,
        branch: str = "main"
    ):
        if repository == "67":
            await interaction.response.send_message("You don't deserve the bot's functionality")
            return


        deferred: bool = False
        repo_name: str = repository
        branch_name: str = ""
        url: str = REPOS.get(repository, "")
        if url.startswith("$"): # alias
            repo_name = f"{url.removeprefix('$')} (alias `{repository}`)"
            url = REPOS.get(url.removeprefix("$"), "")
        elif url == "": # empty -> check url
            r_url = f"https://api.github.com/repos/Unnamed-org123/{repository}"
            await interaction.response.defer()
            deferred = True

            # check if a repo exists
            r = requests.get(r_url, headers={"User-Agent": "repo-check"})
            if r.status_code == 200:
                url = f"https://github.com/Unnamed-org123/{repository}"
            else:
                await interaction.followup.send(
                    "This repository does not exist.",
                    ephemeral=True
                )
                return
        
        if branch != "main":
            if not deferred:
                await interaction.response.defer()
                deferred = True

            repo_parts = url.strip("/").split("/")

            if len(repo_parts) < 2:
                print(url)
                print(repo_parts)
                await interaction.response.send_message(
                    "Invalid repository URL."
                )
                return

            repo_url = repo_parts[-2] + "/" + repo_parts[-1]
            
            r_url = f"https://api.github.com/repos/{repo_url}/branches/{branch}"
            r = requests.get(r_url, headers={"User-Agent": "repo-branch-checker"})
            if r.status_code == 200:
                url = f"https://github.com/{repo_url}/tree/{branch}"
                branch_name = branch
            else:
                await interaction.followup.send(
                    f"Repository `{repository}` has no branch `{branch}`",
                    ephemeral=True
                )

        view = discord.ui.View()

        view.add_item(
            discord.ui.Button(
                label=f"Open {repository}",
                url=url
            )
        )

        branch_string: str = f"\nBranch: **{branch_name}**" if branch_name != "" else ""

        embed = discord.Embed(
            title="Repository",
            description=f"Repository: **{repo_name}**{branch_string}",
            color=discord.Color.from_str("#676767")
        )

        embed.add_field(
            name="URL",
            value=url,
            inline=False
        )

        if deferred:
            await interaction.followup.send(
                embed=embed,
                view=view
            )
        else:
            await interaction.response.send_message(
                embed=embed,
                view=view
            )
    
    @tree.command(
        name="package",
        description="Get a link to a Vexil package"
    )
    async def package(
        interaction: discord.Interaction,
        package: str,
    ):
        if package == "67":
            await interaction.response.send_message("You don't deserve the bot's functionality")
            return


        await interaction.response.defer()

        REGISTRY_URL: str = "https://raw.githubusercontent.com/Unnamed-org123/Registry/refs/heads/main/Packages.json"

        r: requests.Response = requests.get(REGISTRY_URL)
        if r.status_code != 200:
            await interaction.followup.send(
                "Failed to get registry packages!",
                ephemeral=True
            )
            return
        
        package = package.lower()

        packages: dict[str, str] = r.json()
        packages = {k.lower(): v for k, v in packages.items()}

        if package not in packages.keys():
            await interaction.followup.send(
                "Couldn't find this package!",
                ephemeral=True
            )
            return
        
        url: str = packages[package]

        view = discord.ui.View()

        view.add_item(
            discord.ui.Button(
                label=f"Open {package}",
                url=url
            )
        )

        embed: discord.Embed = discord.Embed(
            title="Package",
            description=f"Package: **{package}**",
            color=discord.Color.from_str("#676767")
        )

        embed.add_field(
            name="URL",
            value=url,
            inline=False
        )

        await interaction.followup.send(
            embed=embed,
            view=view
        )