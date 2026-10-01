from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    environment: str = "development"
    demo_mode: bool = True

    gemini_api_key: str = ""
    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-pro"

    image_provider: str = "demo"
    hf_token: str = ""
    hf_image_model: str = "stable-diffusion-v1-5/stable-diffusion-v1-5"
    local_image_model: str = "stable-diffusion-v1-5/stable-diffusion-v1-5"
    image_width: int = 768
    image_height: int = 512
    image_steps: int = 25
    image_guidance: float = 7.5

    max_panels: int = 5
    output_dir: str = "static/panels"
    export_dir: str = "static/exports"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8",
        case_sensitive=False, extra="ignore"
    )

    @property
    def root_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    @property
    def panels_dir(self) -> Path:
        return self.root_dir / self.output_dir

    @property
    def exports_dir(self) -> Path:
        return self.root_dir / self.export_dir

    def ensure_directories(self) -> None:
        self.panels_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings
