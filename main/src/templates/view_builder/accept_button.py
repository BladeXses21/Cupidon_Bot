from discord.ui import View

from templates.button.buttons import buttons
from templates.localization.translations import translate_text


class StartConfirmation(View):
    def __init__(self, control_panel, language):
        super().__init__(timeout=None)
        buttons.accept_button.label = translate_text('click', language)
        buttons.accept_button.callback = control_panel
        self.add_item(buttons.accept_button)
