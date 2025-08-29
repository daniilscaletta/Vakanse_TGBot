import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:

    BOT_TOKEN: Optional[str] = os.getenv("BOT_TOKEN", "")
    API_HOST: str = os.getenv("HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("PORT", "8000"))
    MAX_VACANCIES: int = int(os.getenv("MAX_VACANCIES", "20"))
    NOTIFICATION_USER_ID: Optional[int] = os.getenv("USER_ID", "")
    
    
    
    @classmethod
    def validate(cls) -> None:
        if not cls.BOT_TOKEN:
            raise ValueError(
                "BOT_TOKEN environment variable is required. "
                "Set it to your Telegram bot token from @BotFather"
            )
        
        if cls.BOT_TOKEN == "your_bot_token_here":
            raise ValueError(
                "Please set a real BOT_TOKEN in environment variables. "
                "Get your token from @BotFather in Telegram"
            )

config = Config()
