import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio


TOKEN = "TON_TOKEN"  
ROLE_TANA_MEC = 1363940558401310901
ROLE_TANA_MEUF = 1363940639846306174
AUTO_ROLE_ID = 1232345744716075161 
WELCOME_CHANNEL_ID = 1363925565731766585  


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="🎟️ Créez un Ticket de Support",
        description=( 
            "Tu rencontres un problème, tu as une question ou besoin d’un membre du staff ?\n"
            "Ouvre un ticket en cliquant sur le bouton ci-dessous. Un salon privé sera créé où tu pourras discuter directement avec l’équipe.\n"
            "Merci de bien expliquer ta demande dès le début pour qu’on puisse t’aider le plus vite possible ✅"
        ),
        color=discord.Color.blue()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/950038001491275786/1363987096519315506/image.png?ex=68080779&is=6806b5f9&hm=4d9d5a782bd9884701683b3f83d9ee723db4d952383bfee8ef6a54fe717384d0&")

    button = Button(label="Ouvrir un ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    view = View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)


@bot.command(name="roleselection")
async def send_role_selection(ctx):
    embed = discord.Embed(
        title="🎉 Bienvenue sur le serveur !",
        description="Clique sur un des boutons ci-dessous pour choisir ton rôle.",
        color=discord.Color.blue()
    )

    class RoleButtons(View):
        @discord.ui.button(label="Tana mec", style=discord.ButtonStyle.primary)
        async def tana_mec(self, interaction: discord.Interaction, button: Button):
            role = interaction.guild.get_role(ROLE_TANA_MEC)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("✅ Tu as reçu le rôle **Tana mec** !", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Rôle introuvable.", ephemeral=True)

        @discord.ui.button(label="Tana meuf", style=discord.ButtonStyle.secondary)
        async def tana_meuf(self, interaction: discord.Interaction, button: Button):
            role = interaction.guild.get_role(ROLE_TANA_MEUF)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("✅ Tu as reçu le rôle **Tana meuf** !", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Rôle introuvable.", ephemeral=True)

    await ctx.send(embed=embed, view=RoleButtons())


@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component:
        custom_id = interaction.data.get("custom_id")

        if custom_id == "open_ticket":
            guild = interaction.guild
            member = interaction.user

            ticket_channel = await guild.create_text_channel(
                f"ticket-{member.name}",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(view_channel=True),
                }
            )

            embed_ticket = discord.Embed(
                title="Votre Ticket",
                description=f"Salut {member.mention}, voici ton ticket ! Un membre du staff va venir t'aider sous peu.",
                color=discord.Color.green()
            )

            close_button = Button(label="Fermer le Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
            view = View()
            view.add_item(close_button)

            await ticket_channel.send(embed=embed_ticket, view=view)
            await interaction.response.send_message(f"Ton ticket a été créé ici: {ticket_channel.mention}", ephemeral=True)

        elif custom_id == "close_ticket":
            channel = interaction.channel
            await channel.delete()
            await interaction.response.send_message("Le ticket a été fermé.", ephemeral=True)


@bot.event
async def on_member_join(member):
   
    role = discord.utils.get(member.guild.roles, id=AUTO_ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f"Le rôle {role.name} a été attribué à {member.name}.")
    else:
        print("Rôle introuvable.")

   
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel:
        await welcome_channel.send(f"🎉 Bienvenue {member.mention} sur le serveur !")


@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")


bot.run(TOKEN)
