import dataclasses

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class SlideshowControllerConfig(BaseConfig):
    slideshow_path: str = None
    python_path: str = None
    configs_path: str = None
    main_path: str = None
    args: list[str] = None
