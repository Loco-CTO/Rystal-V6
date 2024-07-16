import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from config.config import lang, lang_mapping, langs
from database.guild_handler import (change_guild_language, change_guild_settings, get_guild_language,
                                    get_guild_settings)
from module.embed import Embeds

class_namespace = "setting_class_title"


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        description="⚙️ | Setting"
    )
    async def setting(
        self,
        interaction: Interaction,
    ):
        return

    @setting.subcommand(description="⚙️ | Change the bot language in this server!")
    async def language(
        self,
        interaction: Interaction,
        language: str = SlashOption(name="language", choices=langs, required=True),
    ):
        await interaction.response.defer(with_message=True)

        try:
            await change_guild_language(interaction.guild.id, lang_mapping[language])

            await interaction.followup.send(
                embed=Embeds.message(
                    title=lang[await get_guild_language(interaction.guild.id)][
                        class_namespace
                    ],
                    message=lang[await get_guild_language(interaction.guild.id)][
                        "language_changed"
                    ].format(language=language),
                    message_type="info",
                )
            )
        except Exception:
            await interaction.followup.send(
                embed=Embeds.message(
                    title=lang[await get_guild_language(interaction.guild.id)][
                        class_namespace
                    ],
                    message=lang[await get_guild_language(interaction.guild.id)][
                        "unknown_error"
                    ],
                    message_type="error",
                )
            )

    @setting.subcommand(
        description="🎵 | Toggle silent mode in this server! (Mutes track-start notification)"
    )
    async def silent_mode(self, interaction: Interaction):
        await interaction.response.defer(with_message=True)
        toggle = not (
            await get_guild_settings(interaction.guild.id, "music_silent_mode")
        )

        await change_guild_settings(interaction.guild.id, "music_silent_mode", toggle)

        toggle_represent = {
            True : "on",
            False: "off",
        }

        await interaction.followup.send(
            embed=Embeds.message(
                title=lang[await get_guild_language(interaction.guild.id)][
                    class_namespace
                ],
                message=lang[await get_guild_language(interaction.guild.id)][
                    "toggle_silent_mode"
                ].format(toggle=toggle_represent[toggle]),
                message_type="info",
            )
        )

    @setting.subcommand(
        description="🎵 | Toggle leave when voice channel is empty in this server!"
    )
    async def auto_leave(self, interaction: Interaction):
        await interaction.response.defer(with_message=True)
        toggle = not (
            await get_guild_settings(interaction.guild.id, "music_auto_leave")
        )

        await change_guild_settings(interaction.guild.id, "music_auto_leave", toggle)

        toggle_represent = {
            True : "on",
            False: "off",
        }

        await interaction.followup.send(
            embed=Embeds.message(
                title=lang[await get_guild_language(interaction.guild.id)][
                    class_namespace
                ],
                message=lang[await get_guild_language(interaction.guild.id)][
                    "toggle_auto_leave"
                ].format(toggle=toggle_represent[toggle]),
                message_type="info",
            )
        )


async def setup(bot):
    bot.add_cog(Settings(bot))
