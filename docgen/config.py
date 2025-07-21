import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from enum import Enum

from pathlib import Path

# ---- Types Customisés ----
class ThresholdsConfig(BaseModel):
    warning: float = Field(..., ge=0, le=100)
    critical: float = Field(..., ge=0, le=100)
    spike: Optional[float] = Field(None, ge=0, le=100)

class ResourceType(str, Enum):
    CPU = "cpu"
    RAM = "ram"
    DISK = "disk"
    TEMP = "temp"
    GPU = "gpu"
    BATTERY = "battery"

# ---- Modèle Principal ----
class Config(BaseModel):
    """Configuration centralisée avec validation et hot-reload."""
    
    # Groq
    groq_api_key: str = Field(default=..., description="Clé API Groq")
    groq_models: List[str] = Field(default=["llama3-70b-8192"])
    groq_temperature: float = Field(default=0.3, ge=0, le=1)
    groq_max_tokens: int = Field(default=100, ge=10)
    

    # TTS
    tts_endpoints: Dict[str, str] = Field(
        default={
            "voices": "https://low-tts.onrender.com/api/voices-by-text",
            "generate": "https://low-tts.onrender.com/api/tts"
        }
    )
    tts_timeout: int = Field(default=30, ge=5)
    tts_voice_preference: List[str] = Field(default=["fr-FR"])
    
    # Audio
    audio_volume: float = Field(default=0.8, ge=0, le=1)

# ---- Chargement Dynamique ----
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_config()
        return cls._instance
    
    def _init_config(self):
        """Charge la config depuis YAML ou .env"""
        load_dotenv()
        self.config = Config(
                groq_api_key=os.getenv("GROQ_API_KEY", ""),
                groq_models=["llama3-70b-8192"],
                groq_temperature=0.3,
                groq_max_tokens=100,
                tts_timeout=30,
                audio_volume=0.8
            )

# ---- Singleton Global ----
config = ConfigManager().config