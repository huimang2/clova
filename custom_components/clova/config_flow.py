"""Config flow for Clova Home EX"""

from homeassistant import config_entries
from .const import DOMAIN, SIDEBAR_TITLE


class ClovaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Clova Home EX """

    VERSION = 1

    async def async_step_import(self, user_input):
        """ Import a config entry. """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title=SIDEBAR_TITLE, data={})