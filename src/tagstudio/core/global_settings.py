# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio

import sys
from pathlib import Path

import toml
from pydantic import BaseModel, Field

if sys.platform == "win32":
    DEFAULT_SETTINGS_PATH = Path.home() / "Appdata" / "Roaming" / "TagStudio" / "settings.toml"
else:
    DEFAULT_SETTINGS_PATH = Path.home() / ".config" / "TagStudio" / "settings.toml"


# NOTE: pydantic also has a BaseSettings class (from pydantic-settings) that allows any settings
# properties to be overwritten with environment variables. as tagstudio is not currently using
# environment variables, i did not base it on that, but that may be useful in the future.
class GlobalSettings(BaseModel):
    # TODO: dark mode, page size
    language: str = Field(default="en")

    # settings from the old SettingItems enum
    open_last_loaded_on_startup: bool = Field(default=False)
    show_library_list: bool = Field(default=True)
    autoplay: bool = Field(default=False)
    show_filenames_in_grid: bool = Field(default=False)

    @staticmethod
    def read_settings(path: Path = DEFAULT_SETTINGS_PATH) -> "GlobalSettings":
        if path.exists():
            with open(path) as file:
                filecontents = file.read()
                if len(filecontents.strip()) != 0:
                    settings_data = toml.loads(filecontents)
                    settings = GlobalSettings(**settings_data)
                    return settings

        return GlobalSettings()

    def save(self, path: Path = DEFAULT_SETTINGS_PATH) -> None:
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            toml.dump(dict(self), f)
