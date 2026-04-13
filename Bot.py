# “””
VR Modding Discord Bot — Slash Command Edition

All commands use Discord’s native / slash commands.

Requirements:
pip install discord.py

Setup:
1. Go to https://discord.com/developers/applications
2. Create a New Application → Bot tab → Reset Token → copy it
3. Enable under Bot > Privileged Gateway Intents:
✅ SERVER MEMBERS INTENT
✅ MESSAGE CONTENT INTENT
4. Invite URL (OAuth2 > URL Generator):
Scopes:      bot  +  applications.commands
Permissions: Administrator
5. Paste your token below OR set env var DISCORD_TOKEN

Note on slash command sync:
On first run the bot calls sync() globally. Commands may take
up to 1 hour to appear everywhere. For instant testing during
development, set GUILD_ID to your server’s ID (see below).
“””

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────────

TOKEN = os.getenv(“DISCORD_TOKEN”, “YOUR_BOT_TOKEN_HERE”)

# Optional: set to your server’s ID (int) for instant slash command sync

# during development. Set to None for global sync.

# Example: GUILD_ID = 1234567890123456789

GUILD_ID = None

# ──────────────────────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=”§”, intents=intents)  # prefix unused but required
tree = bot.tree

# ─── ROLE DEFINITIONS ─────────────────────────────────────────────────────────

ROLES = [
{“name”: “Owner”,          “color”: 0xFF0000, “hoist”: True,  “mentionable”: False, “permissions”: discord.Permissions(administrator=True)},
{“name”: “Admin”,          “color”: 0xFF4500, “hoist”: True,  “mentionable”: True,  “permissions”: discord.Permissions(administrator=True)},
{“name”: “Moderator”,      “color”: 0xFF8C00, “hoist”: True,  “mentionable”: True,  “permissions”: discord.Permissions(manage_messages=True, kick_members=True, ban_members=True, manage_channels=True)},
{“name”: “Trial Mod”,      “color”: 0xFFA500, “hoist”: True,  “mentionable”: True,  “permissions”: discord.Permissions(manage_messages=True)},
{“name”: “⭐ Supporter”,   “color”: 0xFFD700, “hoist”: True,  “mentionable”: True,  “permissions”: discord.Permissions.none()},
{“name”: “🔧 Developer”,  “color”: 0x00BFFF, “hoist”: True,  “mentionable”: True,  “permissions”: discord.Permissions.none()},
{“name”: “🎮 VR Veteran”,  “color”: 0x9B59B6, “hoist”: True,  “mentionable”: True,  “permissions”: discord.Permissions.none()},
{“name”: “Modder”,         “color”: 0x2ECC71, “hoist”: False, “mentionable”: True,  “permissions”: discord.Permissions.none()},
{“name”: “Tester”,         “color”: 0x1ABC9C, “hoist”: False, “mentionable”: True,  “permissions”: discord.Permissions.none()},
{“name”: “Avatar Creator”, “color”: 0xE91E63, “hoist”: False, “mentionable”: True,  “permissions”: discord.Permissions.none()},
{“name”: “World Builder”,  “color”: 0x3498DB, “hoist”: False, “mentionable”: True,  “permissions”: discord.Permissions.none()},
{“name”: “Skid/Larp”,      “color”: 0x808080, “hoist”: False, “mentionable”: False, “permissions”: discord.Permissions.none()},
{“name”: “🤖 Bot”,         “color”: 0x5865F2, “hoist”: True,  “mentionable”: False, “permissions”: discord.Permissions.none()},
]

# ─── CHANNEL STRUCTURE ────────────────────────────────────────────────────────

CHANNEL_STRUCTURE = [
{
“category”: “📋 INFORMATION”,
“channels”: [
{“name”: “📌│rules”,          “type”: “text”,  “topic”: “Read before participating. Ignorance is not an excuse.”, “read_only”: True},
{“name”: “📣│announcements”,  “type”: “text”,  “topic”: “Server announcements and updates.”, “read_only”: True},
{“name”: “🆕│changelog”,      “type”: “text”,  “topic”: “Mod and server changelogs.”, “read_only”: True},
{“name”: “🎫│roles”,          “type”: “text”,  “topic”: “Self-assign roles here.”, “read_only”: True},
{“name”: “❓│faq”,            “type”: “text”,  “topic”: “Frequently asked questions about VR modding.”, “read_only”: True},
],
},
{
“category”: “💛 SUPPORTER LOUNGE”,
“channels”: [
{“name”: “🛒│buy-supporter”,  “type”: “text”,  “topic”: “Support the server and unlock exclusive perks!”, “read_only”: True, “supporter_buy”: True},
{“name”: “⭐│supporter-chat”, “type”: “text”,  “topic”: “Exclusive chat for supporters.”, “supporter_only”: True},
{“name”: “🔒│supporter-mods”, “type”: “text”,  “topic”: “Exclusive mods and early access drops for supporters.”, “supporter_only”: True},
{“name”: “🎙│supporter-vc”,   “type”: “voice”, “supporter_only”: True},
],
},
{
“category”: “💬 GENERAL”,
“channels”: [
{“name”: “💬│general”,        “type”: “text”,  “topic”: “General VR talk and off-topic.”},
{“name”: “🎮│vr-chat”,        “type”: “text”,  “topic”: “Talk about VRChat specifically.”},
{“name”: “📸│media-showcase”, “type”: “text”,  “topic”: “Share screenshots, clips and art.”},
{“name”: “😂│memes”,          “type”: “text”,  “topic”: “VR memes only.”},
{“name”: “🤖│bot-commands”,   “type”: “text”,  “topic”: “Use bot commands here.”},
],
},
{
“category”: “🔧 MODDING HUB”,
“channels”: [
{“name”: “📦│mod-releases”,   “type”: “text”,  “topic”: “Post your mod releases here. Use the pinned format.”},
{“name”: “🛠│mod-help”,       “type”: “text”,  “topic”: “Ask modding questions. Be specific and include logs.”},
{“name”: “💡│mod-ideas”,      “type”: “text”,  “topic”: “Pitch mod ideas for others to create.”},
{“name”: “🐛│bug-reports”,    “type”: “text”,  “topic”: “Report bugs for mods in this server.”},
{“name”: “🧪│mod-testing”,    “type”: “text”,  “topic”: “Beta testing and feedback for unreleased mods.”},
],
},
{
“category”: “🎨 CREATION”,
“channels”: [
{“name”: “🧍│avatar-releases”,“type”: “text”,  “topic”: “Share avatar releases. Include platform and SDK version.”},
{“name”: “🌍│world-releases”, “type”: “text”,  “topic”: “Share world releases.”},
{“name”: “🎨│avatar-help”,    “type”: “text”,  “topic”: “Questions about avatar creation, Unity, Blender, etc.”},
{“name”: “🌐│world-help”,     “type”: “text”,  “topic”: “Questions about world creation and SDK.”},
{“name”: “📚│resources”,      “type”: “text”,  “topic”: “Tutorials, tools, and useful links.”, “read_only”: True},
],
},
{
“category”: “🎙 VOICE”,
“channels”: [
{“name”: “🔊│General VC”,     “type”: “voice”},
{“name”: “🎮│Gaming VC”,      “type”: “voice”},
{“name”: “🛠│Modding VC”,     “type”: “voice”},
{“name”: “🎵│Music VC”,       “type”: “voice”},
{“name”: “🔕│AFK”,            “type”: “voice”},
],
},
{
“category”: “🛡 STAFF”,
“channels”: [
{“name”: “📋│staff-chat”,     “type”: “text”,  “topic”: “Staff only discussion.”, “staff_only”: True},
{“name”: “📝│mod-logs”,       “type”: “text”,  “topic”: “Moderation action logs.”, “staff_only”: True},
{“name”: “🔨│ban-appeals”,    “type”: “text”,  “topic”: “Ban appeal intake.”, “staff_only”: True},
{“name”: “🎙│staff-vc”,       “type”: “voice”, “staff_only”: True},
],
},
]

SUPPORTER_EMBED_TEXT = (
“# ⭐ Become a Supporter!\n\n”
“Help keep the server running and unlock exclusive perks:\n\n”
“✅ **Exclusive `⭐ Supporter` role** (shows in member list)\n”
“✅ Access to **#supporter-chat** and **#supporter-mods**\n”
“✅ Early access to unreleased mods and avatars\n”
“✅ Exclusive supporter-only voice channel\n”
“✅ Priority support from staff\n”
“✅ Warm fuzzy feelings ✨\n\n”
“**How to get it:**\n”
“> DM an **Admin** or **Owner** to purchase.\n”
“> Payment via Ko-fi, PayPal, or other agreed method.\n\n”
“*Thank you for keeping this community alive! 💛*”
)

# ─── SERVER BUILD HELPER ──────────────────────────────────────────────────────

async def _build_server(guild: discord.Guild) -> dict:
“”“Wipe and rebuild the entire server. Returns stats dict.”””

```
for role in list(guild.roles):
    if role.name != "@everyone" and not role.managed:
        try:
            await role.delete()
            await asyncio.sleep(0.4)
        except Exception:
            pass

for channel in list(guild.channels):
    try:
        await channel.delete()
        await asyncio.sleep(0.3)
    except Exception:
        pass

await asyncio.sleep(1)

created_roles: dict[str, discord.Role] = {}
for role_data in reversed(ROLES):
    r = await guild.create_role(
        name=role_data["name"],
        color=discord.Color(role_data["color"]),
        hoist=role_data["hoist"],
        mentionable=role_data["mentionable"],
        permissions=role_data.get("permissions", discord.Permissions.none()),
    )
    created_roles[role_data["name"]] = r
    await asyncio.sleep(0.4)

supporter_role = created_roles.get("⭐ Supporter")
staff_roles = [
    r for name in ("Owner", "Admin", "Moderator", "Trial Mod")
    if (r := created_roles.get(name))
]
everyone = guild.default_role

buy_supporter_channel = None

for cat_data in CHANNEL_STRUCTURE:
    is_staff_cat     = any(c.get("staff_only")     for c in cat_data["channels"])
    is_supporter_cat = any(c.get("supporter_only") for c in cat_data["channels"])

    cat_ow: dict = {everyone: discord.PermissionOverwrite(read_messages=True)}
    if is_staff_cat:
        cat_ow[everyone] = discord.PermissionOverwrite(read_messages=False)
        for sr in staff_roles:
            cat_ow[sr] = discord.PermissionOverwrite(read_messages=True)
    if is_supporter_cat:
        cat_ow[everyone] = discord.PermissionOverwrite(read_messages=False)
        if supporter_role:
            cat_ow[supporter_role] = discord.PermissionOverwrite(read_messages=True)
        for sr in staff_roles:
            cat_ow[sr] = discord.PermissionOverwrite(read_messages=True)

    category = await guild.create_category(cat_data["category"], overwrites=cat_ow)
    await asyncio.sleep(0.3)

    for ch in cat_data["channels"]:
        ow: dict = {}
        if ch.get("staff_only"):
            ow[everyone] = discord.PermissionOverwrite(read_messages=False)
            for sr in staff_roles:
                ow[sr] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        elif ch.get("supporter_only"):
            ow[everyone] = discord.PermissionOverwrite(read_messages=False)
            if supporter_role:
                ow[supporter_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            for sr in staff_roles:
                ow[sr] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        elif ch.get("supporter_buy"):
            ow[everyone] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
            for sr in staff_roles:
                ow[sr] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        elif ch.get("read_only"):
            ow[everyone] = discord.PermissionOverwrite(send_messages=False)
            for sr in staff_roles:
                ow[sr] = discord.PermissionOverwrite(send_messages=True)

        if ch["type"] == "voice":
            channel = await guild.create_voice_channel(ch["name"], category=category, overwrites=ow)
        else:
            channel = await guild.create_text_channel(
                ch["name"], category=category,
                topic=ch.get("topic", ""), overwrites=ow,
            )

        if ch.get("supporter_buy"):
            buy_supporter_channel = channel

        await asyncio.sleep(0.35)

if buy_supporter_channel:
    await buy_supporter_channel.send(SUPPORTER_EMBED_TEXT)

return {"roles": len(created_roles)}
```

# ─── /setup ───────────────────────────────────────────────────────────────────

@tree.command(name=“setup”, description=“⚙️ Fully set up this server as a VR modding server (Admin only)”)
@app_commands.checks.has_permissions(administrator=True)
async def slash_setup(interaction: discord.Interaction):
await interaction.response.send_message(
“🔧 Setting up the server… this will take ~30–60 seconds. Don’t close Discord!”,
ephemeral=True,
)
try:
stats = await _build_server(interaction.guild)
await interaction.followup.send(
f”✅ **Server setup complete!**\n”
f”• {stats[‘roles’]} roles created\n”
f”• All categories and channels built\n”
f”• Supporter channel populated\n\n”
f”**Next steps:**\n”
f”1. Assign `Owner` role to yourself\n”
f”2. Add your payment link to `#buy-supporter`\n”
f”3. Set a server icon and banner\n”
f”4. Invite your community! 🎉”,
ephemeral=True,
)
except Exception as e:
await interaction.followup.send(f”❌ Setup failed: `{e}`”, ephemeral=True)

# ─── /supporter ───────────────────────────────────────────────────────────────

@tree.command(name=“supporter”, description=“⭐ Show supporter perks and how to get the role”)
async def slash_supporter(interaction: discord.Interaction):
embed = discord.Embed(
title=“⭐ Supporter Perks”,
description=SUPPORTER_EMBED_TEXT,
color=discord.Color.gold(),
)
embed.set_footer(text=“DM an Admin or Owner to purchase.”)
await interaction.response.send_message(embed=embed)

# ─── /givesupporter ───────────────────────────────────────────────────────────

@tree.command(name=“givesupporter”, description=“⭐ Grant the Supporter role to a member (Mod+)”)
@app_commands.describe(member=“The member to give Supporter to”)
@app_commands.checks.has_permissions(manage_roles=True)
async def slash_give_supporter(interaction: discord.Interaction, member: discord.Member):
role = discord.utils.get(interaction.guild.roles, name=“⭐ Supporter”)
if not role:
await interaction.response.send_message(“❌ Supporter role not found. Run `/setup` first.”, ephemeral=True)
return
if role in member.roles:
await interaction.response.send_message(f”ℹ️ {member.mention} already has Supporter.”, ephemeral=True)
return
await member.add_roles(role)
embed = discord.Embed(description=f”⭐ {member.mention} is now a **Supporter**!”, color=discord.Color.gold())
await interaction.response.send_message(embed=embed)
try:
await member.send(
f”⭐ You’ve been granted **Supporter** in **{interaction.guild.name}**!\n”
f”You now have access to exclusive supporter channels. Thanks! 💛”
)
except discord.Forbidden:
pass

# ─── /removesupporter ─────────────────────────────────────────────────────────

@tree.command(name=“removesupporter”, description=“🚫 Remove the Supporter role from a member (Mod+)”)
@app_commands.describe(member=“The member to remove Supporter from”)
@app_commands.checks.has_permissions(manage_roles=True)
async def slash_remove_supporter(interaction: discord.Interaction, member: discord.Member):
role = discord.utils.get(interaction.guild.roles, name=“⭐ Supporter”)
if not role:
await interaction.response.send_message(“❌ Supporter role not found.”, ephemeral=True)
return
if role not in member.roles:
await interaction.response.send_message(f”ℹ️ {member.mention} doesn’t have Supporter.”, ephemeral=True)
return
await member.remove_roles(role)
await interaction.response.send_message(f”✅ Removed **Supporter** from {member.mention}.”, ephemeral=True)

# ─── /giverole ────────────────────────────────────────────────────────────────

@tree.command(name=“giverole”, description=“🎭 Give any role to a member (Mod+)”)
@app_commands.describe(member=“The target member”, role=“The role to give”)
@app_commands.checks.has_permissions(manage_roles=True)
async def slash_give_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
if role in member.roles:
await interaction.response.send_message(f”ℹ️ {member.mention} already has **{role.name}**.”, ephemeral=True)
return
await member.add_roles(role)
embed = discord.Embed(description=f”✅ Gave **{role.name}** to {member.mention}.”, color=role.color)
await interaction.response.send_message(embed=embed)

# ─── /removerole ──────────────────────────────────────────────────────────────

@tree.command(name=“removerole”, description=“🗑️ Remove a role from a member (Mod+)”)
@app_commands.describe(member=“The target member”, role=“The role to remove”)
@app_commands.checks.has_permissions(manage_roles=True)
async def slash_remove_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
if role not in member.roles:
await interaction.response.send_message(f”ℹ️ {member.mention} doesn’t have **{role.name}**.”, ephemeral=True)
return
await member.remove_roles(role)
await interaction.response.send_message(f”✅ Removed **{role.name}** from {member.mention}.”, ephemeral=True)

# ─── /serverinfo ──────────────────────────────────────────────────────────────

@tree.command(name=“serverinfo”, description=“📊 Display server statistics”)
async def slash_server_info(interaction: discord.Interaction):
guild = interaction.guild
embed = discord.Embed(title=f”📊 {guild.name}”, color=discord.Color.blurple())
embed.add_field(name=“👥 Members”,   value=guild.member_count,                       inline=True)
embed.add_field(name=“🎭 Roles”,     value=len(guild.roles),                         inline=True)
embed.add_field(name=“📁 Channels”,  value=len(guild.channels),                      inline=True)
embed.add_field(name=“👑 Owner”,     value=str(guild.owner),                         inline=True)
embed.add_field(name=“🌍 Locale”,    value=str(guild.preferred_locale),              inline=True)
embed.add_field(name=“📅 Created”,   value=guild.created_at.strftime(”%b %d, %Y”),   inline=True)
if guild.icon:
embed.set_thumbnail(url=guild.icon.url)
await interaction.response.send_message(embed=embed)

# ─── /userinfo ────────────────────────────────────────────────────────────────

@tree.command(name=“userinfo”, description=“👤 Display info about a member”)
@app_commands.describe(member=“Member to look up (defaults to yourself)”)
async def slash_user_info(interaction: discord.Interaction, member: discord.Member = None):
member = member or interaction.user
roles = [r.mention for r in member.roles if r.name != “@everyone”]
embed = discord.Embed(title=f”👤 {member.display_name}”, color=member.color)
embed.set_thumbnail(url=member.display_avatar.url)
embed.add_field(name=“Username”,    value=str(member),                             inline=True)
embed.add_field(name=“ID”,          value=str(member.id),                          inline=True)
embed.add_field(name=“Joined”,      value=member.joined_at.strftime(”%b %d, %Y”),  inline=True)
embed.add_field(name=“Account Age”, value=member.created_at.strftime(”%b %d, %Y”), inline=True)
embed.add_field(name=f”Roles ({len(roles)})”, value=” “.join(roles) or “None”,     inline=False)
await interaction.response.send_message(embed=embed)

# ─── /announce ────────────────────────────────────────────────────────────────

@tree.command(name=“announce”, description=“📣 Post an announcement embed (Admin+)”)
@app_commands.describe(
title=“Announcement title”,
message=“Announcement body”,
channel=“Channel to post in (defaults to current)”,
ping_everyone=“Whether to ping @everyone”,
)
@app_commands.checks.has_permissions(administrator=True)
async def slash_announce(
interaction: discord.Interaction,
title: str,
message: str,
channel: discord.TextChannel = None,
ping_everyone: bool = False,
):
target = channel or interaction.channel
embed = discord.Embed(title=f”📣 {title}”, description=message, color=discord.Color.orange())
embed.set_footer(text=f”Posted by {interaction.user.display_name}”)
content = “@everyone” if ping_everyone else None
await target.send(content=content, embed=embed)
await interaction.response.send_message(f”✅ Announcement posted in {target.mention}.”, ephemeral=True)

# ─── /purge ───────────────────────────────────────────────────────────────────

@tree.command(name=“purge”, description=“🗑️ Bulk delete messages in this channel (Mod+)”)
@app_commands.describe(amount=“Number of messages to delete (1–100)”)
@app_commands.checks.has_permissions(manage_messages=True)
async def slash_purge(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
await interaction.response.defer(ephemeral=True)
deleted = await interaction.channel.purge(limit=amount)
await interaction.followup.send(f”🗑️ Deleted **{len(deleted)}** messages.”, ephemeral=True)

# ─── /kick ────────────────────────────────────────────────────────────────────

@tree.command(name=“kick”, description=“👢 Kick a member from the server (Mod+)”)
@app_commands.describe(member=“Member to kick”, reason=“Reason for kick”)
@app_commands.checks.has_permissions(kick_members=True)
async def slash_kick(interaction: discord.Interaction, member: discord.Member, reason: str = “No reason provided”):
if member.top_role >= interaction.user.top_role:
await interaction.response.send_message(“❌ You can’t kick someone with an equal or higher role.”, ephemeral=True)
return
await member.kick(reason=reason)
embed = discord.Embed(
description=f”👢 **{member}** was kicked.\n**Reason:** {reason}”,
color=discord.Color.orange(),
)
await interaction.response.send_message(embed=embed)
try:
await member.send(f”You were kicked from **{interaction.guild.name}**.\nReason: {reason}”)
except discord.Forbidden:
pass

# ─── /ban ─────────────────────────────────────────────────────────────────────

@tree.command(name=“ban”, description=“🔨 Ban a member from the server (Mod+)”)
@app_commands.describe(member=“Member to ban”, reason=“Reason for ban”, delete_days=“Days of messages to delete (0–7)”)
@app_commands.checks.has_permissions(ban_members=True)
async def slash_ban(
interaction: discord.Interaction,
member: discord.Member,
reason: str = “No reason provided”,
delete_days: app_commands.Range[int, 0, 7] = 0,
):
if member.top_role >= interaction.user.top_role:
await interaction.response.send_message(“❌ You can’t ban someone with an equal or higher role.”, ephemeral=True)
return
try:
await member.send(f”You were banned from **{interaction.guild.name}**.\nReason: {reason}”)
except discord.Forbidden:
pass
await member.ban(reason=reason, delete_message_days=delete_days)
embed = discord.Embed(
description=f”🔨 **{member}** was banned.\n**Reason:** {reason}”,
color=discord.Color.red(),
)
await interaction.response.send_message(embed=embed)

# ─── /unban ───────────────────────────────────────────────────────────────────

@tree.command(name=“unban”, description=“🔓 Unban a user by their ID (Mod+)”)
@app_commands.describe(user_id=“The Discord user ID to unban”, reason=“Reason for unban”)
@app_commands.checks.has_permissions(ban_members=True)
async def slash_unban(interaction: discord.Interaction, user_id: str, reason: str = “No reason provided”):
try:
user = await bot.fetch_user(int(user_id))
await interaction.guild.unban(user, reason=reason)
await interaction.response.send_message(f”✅ Unbanned **{user}**.”, ephemeral=True)
except discord.NotFound:
await interaction.response.send_message(“❌ User not found or not banned.”, ephemeral=True)
except ValueError:
await interaction.response.send_message(“❌ Invalid user ID.”, ephemeral=True)

# ─── /timeout ─────────────────────────────────────────────────────────────────

@tree.command(name=“timeout”, description=“⏱️ Timeout a member (Mod+)”)
@app_commands.describe(member=“Member to timeout”, minutes=“Duration in minutes (1–10080)”, reason=“Reason”)
@app_commands.checks.has_permissions(moderate_members=True)
async def slash_timeout(
interaction: discord.Interaction,
member: discord.Member,
minutes: app_commands.Range[int, 1, 10080],
reason: str = “No reason provided”,
):
until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
await member.timeout(until, reason=reason)
embed = discord.Embed(
description=f”⏱️ {member.mention} timed out for **{minutes} min**.\n**Reason:** {reason}”,
color=discord.Color.yellow(),
)
await interaction.response.send_message(embed=embed)

# ─── /untimeout ───────────────────────────────────────────────────────────────

@tree.command(name=“untimeout”, description=“✅ Remove a timeout from a member (Mod+)”)
@app_commands.describe(member=“Member to untimeout”)
@app_commands.checks.has_permissions(moderate_members=True)
async def slash_untimeout(interaction: discord.Interaction, member: discord.Member):
await member.timeout(None)
await interaction.response.send_message(f”✅ Removed timeout from {member.mention}.”, ephemeral=True)

# ─── /warn ────────────────────────────────────────────────────────────────────

@tree.command(name=“warn”, description=“⚠️ Send a warning to a member via DM (Mod+)”)
@app_commands.describe(member=“Member to warn”, reason=“Reason for warning”)
@app_commands.checks.has_permissions(manage_messages=True)
async def slash_warn(interaction: discord.Interaction, member: discord.Member, reason: str):
embed = discord.Embed(
title=“⚠️ Warning Issued”,
description=f”{member.mention} has been warned.\n**Reason:** {reason}”,
color=discord.Color.yellow(),
)
embed.set_footer(text=f”Issued by {interaction.user.display_name}”)
await interaction.response.send_message(embed=embed)
try:
await member.send(
f”⚠️ You received a warning in **{interaction.guild.name}**.\n”
f”**Reason:** {reason}\n\nPlease review the server rules.”
)
except discord.Forbidden:
pass

# ─── /help ────────────────────────────────────────────────────────────────────

@tree.command(name=“help”, description=“📖 List all bot slash commands”)
async def slash_help(interaction: discord.Interaction):
embed = discord.Embed(
title=“👾 VR Mod Bot — Slash Commands”,
color=discord.Color.blurple(),
)
embed.add_field(name=“⚙️ Setup”,
value=”`/setup` — Build the full VR modding server *(Admin)*”, inline=False)
embed.add_field(name=“⭐ Supporter”,
value=(
“`/supporter` — Show supporter perks\n”
“`/givesupporter <member>` — Grant Supporter role *(Mod+)*\n”
“`/removesupporter <member>` — Remove Supporter role *(Mod+)*”
), inline=False)
embed.add_field(name=“🎭 Roles”,
value=(
“`/giverole <member> <role>` — Give a role *(Mod+)*\n”
“`/removerole <member> <role>` — Remove a role *(Mod+)*”
), inline=False)
embed.add_field(name=“📋 Info”,
value=(
“`/serverinfo` — Server stats\n”
“`/userinfo [member]` — Member info”
), inline=False)
embed.add_field(name=“🛡️ Moderation”,
value=(
“`/warn <member> <reason>` — Warn via DM *(Mod+)*\n”
“`/kick <member> [reason]` — Kick *(Mod+)*\n”
“`/ban <member> [reason]` — Ban *(Mod+)*\n”
“`/unban <user_id> [reason]` — Unban by ID *(Mod+)*\n”
“`/timeout <member> <minutes>` — Timeout *(Mod+)*\n”
“`/untimeout <member>` — Remove timeout *(Mod+)*\n”
“`/purge <amount>` — Bulk delete messages *(Mod+)*”
), inline=False)
embed.add_field(name=“📣 Announcements”,
value=”`/announce <title> <message>` — Post an embed *(Admin)*”, inline=False)
embed.set_footer(text=“VR Mod Bot • All commands are native Discord slash commands”)
await interaction.response.send_message(embed=embed, ephemeral=True)

# ─── ERROR HANDLER ────────────────────────────────────────────────────────────

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
if isinstance(error, app_commands.MissingPermissions):
msg = “❌ You don’t have permission to use this command.”
elif isinstance(error, app_commands.BotMissingPermissions):
msg = f”❌ I’m missing permissions: `{', '.join(error.missing_permissions)}`”
elif isinstance(error, app_commands.CommandOnCooldown):
msg = f”⏳ Cooldown active. Try again in {error.retry_after:.1f}s.”
else:
msg = f”❌ An error occurred: `{error}`”

```
if interaction.response.is_done():
    await interaction.followup.send(msg, ephemeral=True)
else:
    await interaction.response.send_message(msg, ephemeral=True)
```

# ─── AUTO ROLE ON JOIN ────────────────────────────────────────────────────────

@bot.event
async def on_member_join(member: discord.Member):
role = discord.utils.get(member.guild.roles, name=“Skid/Larp”)
if role:
try:
await member.add_roles(role, reason=“Auto-assigned on join”)
except discord.Forbidden:
pass
try:
await member.send(
f”👾 Welcome to **{member.guild.name}**!\n\n”
f”You’ve been given the `Skid/Larp` role — prove yourself to earn better ones.\n”
f”Check out `#rules` and `#roles` when you arrive!\n\n”
f”*Want exclusive perks? Check out `#buy-supporter`* ⭐”
)
except discord.Forbidden:
pass

# ─── READY + SYNC ─────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
print(f”✅ Logged in as {bot.user} ({bot.user.id})”)

```
if GUILD_ID:
    guild_obj = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild_obj)
    await bot.tree.sync(guild=guild_obj)
    print(f"⚡ Slash commands synced to guild {GUILD_ID} (instant)")
else:
    await bot.tree.sync()
    print("🌐 Slash commands synced globally (may take up to 1 hour to appear)")

await bot.change_presence(
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="VR Mods 👾 | /help"
    )
)
print("   Ready! Type /help in Discord to see all commands.")
```

# ─── RUN ──────────────────────────────────────────────────────────────────────

if **name** == “**main**”:
bot.run(TOKEN)
