import discord.errors
from discord import Interaction
from discord.ui import Select

from config import MIN_AGE, MAX_AGE
from database.system.user_system import user_system
from embed.embeds.base import DefaultEmbed
from embed.embeds.panelEmbed import MainPanelEmbed
from embed.view_builder.accept_button import StartConfirmation
from embed.view_builder.lets_go_button import LetsGoView
from embed.view_builder.main_view_builder import MainMenuView
from message_template.translations import translate_text
from utils.funcs import check_location


class PrivateMessageService:
    def __init__(self, client):
        self.client = client
        self.USER_NAME = str()
        self.USER_AGE = int()
        self.USER_GENDER = str()
        self.USER_LIKE_GENDER = str()
        self.USER_LOCATION = str()
        self.USER_GAMES = str()
        self.USER_DESCRIPTION = str()
        self.USER_PHOTO = str()

        self.function_map = {
            'language_scanning': self.language_scanning,
            'user_name': self.user_name,
            'user_age': self.user_age,
            'user_gender': self.user_gender,
            'like_gender': self.like_gender,
            'user_location': self.user_location,
            'user_games': self.user_games,
            'user_description': self.user_description,
            'user_photo': self.user_photo,
            'form_successfully_created': self.form_successfully_created
        }

        self.function_called = {}

    async def call_function(self, interaction: Interaction, function_name: str):
        if function_name in self.function_map:
            if function_name in self.function_called and self.function_called[function_name]:
                return False

            self.function_called[function_name] = True
            return await self.function_map[function_name](interaction)

    async def language_scanning(self, author):
        view = StartConfirmation(self.presentation_one)
        return await author.send(embed=DefaultEmbed('**click on the button to continue**'), view=view)

    async def presentation_one(self, interaction: Interaction):
        user_language = interaction.locale
        lets_go__view = LetsGoView(self.control_panel, user_language)
        return await interaction.response.send_message(embed=DefaultEmbed(translate_text('Зараз я допоможу тобі знайти пару або прекрасних друзів', user_language)), view=lets_go__view)

    async def presentation_two(self, interaction: Interaction):
        # todo - тут вліпити текст з дайвінчика
        return await interaction.response.send_message(embed=DefaultEmbed('123'))

    async def control_panel(self, interaction: Interaction):
        user_language = interaction.locale

        async def create_form(interact: Interaction):
            return await self.call_function(interaction=interact, function_name='user_name')

        async def look_form(interact: Interaction):
            return await interact.response.send_message(
                embed=DefaultEmbed(description=translate_text('Привіт!', user_language)))

        async def delete_form(interact: Interaction):
            return await interact.response.send_message(
                embed=DefaultEmbed(description=translate_text('Привіт!', user_language)))

        async def share_form(interact: Interaction):
            return await interact.response.send_message(
                embed=DefaultEmbed(description=translate_text('Привіт!', user_language)))

        menu_views = MainMenuView(create_form, look_form, delete_form, share_form)
        return await interaction.response.send_message(embed=MainPanelEmbed(user_language).embed, view=menu_views)

    async def user_name(self, interaction: Interaction):
        user_language = interaction.locale
        await interaction.response.send_message(embed=DefaultEmbed(description=translate_text("Введіть ім'я", user_language)), view=None)

        def check(m):
            if m.channel.id == interaction.channel.id and not m.author.bot:
                return m

        message = await self.client.wait_for('message', check=check)

        if len(message.content) >= 30:
            self.USER_NAME = str(message.content[:30])
            return await self.call_function(interaction=interaction, function_name='user_age')

        else:
            self.USER_NAME = str(message.content)
            return await self.call_function(interaction=interaction, function_name='user_age')

    async def user_age(self, interaction: Interaction):
        user_language = interaction.locale
        await interaction.user.send(embed=DefaultEmbed(translate_text('Скільки тобі років?', interaction.locale), view=None))

        def check(m):
            if m.channel.id == interaction.channel.id and not m.author.bot:
                return m

        message = await self.client.wait_for('message', check=check)

        try:
            age = int(message.content)
            if age < MIN_AGE or age > MAX_AGE:
                return await interaction.followup.send(
                    embed=DefaultEmbed(description=translate_text('Людина вашого віку не може створювати анкету.', user_language)))
            else:
                self.USER_AGE = age
                return await self.call_function(interaction=interaction, function_name='user_gender')
        except ValueError:
            return await interaction.followup.send(embed=DefaultEmbed(description=translate_text('Вік введено некоректно.', user_language)))

    async def user_gender(self, interaction: Interaction):
        user_language = interaction.locale

        async def user_chose_gender(interact: Interaction):
            self.USER_GENDER = select_options.values[0]
            return await self.call_function(interaction=interact, function_name='like_gender')

        gender_options = [
            discord.SelectOption(label=translate_text('Хлопець', user_language), value=translate_text('Хлопець', user_language)),
            discord.SelectOption(label=translate_text('Дівчина', user_language), value=translate_text('Дівчина', user_language)),
            discord.SelectOption(label=translate_text('LGBT', user_language), value=translate_text('LGBT', user_language))
        ]

        select_options = Select(custom_id='gender_selection', options=gender_options, placeholder=translate_text('Оберіть свою стать', user_language),
                                min_values=1, max_values=1)

        view = discord.ui.View(timeout=None)
        view.add_item(select_options)

        select_options.callback = user_chose_gender

        await interaction.followup.send(embed=DefaultEmbed(description=translate_text('Вкажи свою стать:', user_language)), view=view)

    async def like_gender(self, interaction: Interaction):
        user_language = interaction.locale

        async def user_like_gender(interact: Interaction):
            self.USER_LIKE_GENDER = select_options.values[0]
            return await self.call_function(interaction=interact, function_name='user_location')

        gender_options = [
            discord.SelectOption(label=translate_text('Хлопець', user_language), value=translate_text('Хлопець', user_language)),
            discord.SelectOption(label=translate_text('Дівчина', user_language), value=translate_text('Дівчина', user_language)),
            discord.SelectOption(label=translate_text('LGBT', user_language), value=translate_text('LGBT', user_language))
        ]
        select_options = Select(custom_id='like_gender_selection', options=gender_options,
                                placeholder=translate_text('Хто тебе цікавить?', user_language),
                                min_values=1, max_values=1)

        view = discord.ui.View(timeout=None)
        view.add_item(select_options)

        select_options.callback = user_like_gender

        await interaction.response.send_message(embed=DefaultEmbed(description=translate_text('Хто тебе цікавить?', user_language)), view=view)

    async def user_location(self, interaction: Interaction):
        user_language = interaction.locale
        while True:
            try:
                await interaction.response.send_message(embed=DefaultEmbed(description=translate_text('З якого ти міста?', user_language)), view=None)
            except discord.errors.InteractionResponded:
                def check(m):
                    if m.channel.id == interaction.channel.id and not m.author.bot:
                        return m

                message = await self.client.wait_for('message', check=check)

                verification_location = check_location(message.content)
                if verification_location is None:
                    await interaction.user.send(
                        embed=DefaultEmbed(description=translate_text('Локація введена некоректно.\nПовторіть спробу.', user_language)))
                    continue
                else:
                    self.USER_LOCATION = message.content
                    return await self.call_function(interaction=interaction, function_name='user_games')

    async def user_games(self, interaction: Interaction):
        user_language = interaction.locale
        await interaction.user.send(embed=DefaultEmbed(description=translate_text('Введіть ігри в які ви граєте:', user_language)))

        def check(m):
            if m.channel.id == interaction.channel.id and not m.author.bot:
                return m

        message = await self.client.wait_for('message', check=check)

        if len(message.content) >= 75:
            self.USER_GAMES = message.content[:75]
            return await self.call_function(interaction=interaction, function_name='user_description')
        else:
            self.USER_GAMES = message.content
            return await self.call_function(interaction=interaction, function_name='user_description')

    async def user_description(self, interaction: Interaction):
        user_language = interaction.locale
        await interaction.user.send(embed=DefaultEmbed(description=translate_text('Введіть опис профілю:', user_language)))

        while True:
            def check(m):
                if m.channel.id == interaction.channel.id and not m.author.bot:
                    return m

            message = await self.client.wait_for('message', check=check)

            if len(message.content) > 1024:
                await interaction.user.send(embed=DefaultEmbed(description=translate_text('Текст занадто великий, повторіть спробу:', user_language)))
                continue
            else:
                self.USER_DESCRIPTION = message.content
                return await self.call_function(interaction=interaction, function_name='user_photo')

    async def user_photo(self, interaction: Interaction):
        user_language = interaction.locale
        await interaction.user.send(embed=DefaultEmbed(description=translate_text('Загрузіть фото профілю:', user_language)))

        while True:
            def check(m):
                if m.channel.id == interaction.channel.id and not m.author.bot:
                    return m

            message = await self.client.wait_for('message', check=check)

            if len(message.attachments) == 0:
                await interaction.followup.send(
                    embed=DefaultEmbed(description=translate_text('Ви не додали фото профілю. Повторіть спробу.', user_language)))
                continue
            self.USER_PHOTO = str(message.attachments[0])
            return await self.call_function(interaction=interaction, function_name='form_successfully_created')

    async def form_successfully_created(self, interaction: Interaction):
        self.function_called = {}
        user_language = interaction.locale
        user_system.create_user_form(user_id=interaction.user.id, age=self.USER_AGE, gender=self.USER_GENDER, like_gender=self.USER_LIKE_GENDER,
                                     location=self.USER_LOCATION, games=self.USER_GAMES, description=self.USER_DESCRIPTION, photo=self.USER_PHOTO)
        return await interaction.followup.send(embed=DefaultEmbed(description=translate_text('Анкета успішно створена.', user_language)))

# todo - зробити ембед з виведенням даних користувача - показ створеної анкети
