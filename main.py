import atexit
from config import API_ID, API_HASH, BOT_TOKEN
from keep_alive import keep_alive
from data.state import save_all
from pyrogram import Client
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import all handlers
HANDLERS = [
    'handlers.start',
    'handlers.callback',
    'handlers.message',
    'handlers.admin',
    'handlers.stats',
    'handlers.hashtag_search',
    'handlers.voting',
    'handlers.moderasi'
]

def initialize_bot() -> Client:
    """
    Initialize and configure the Pyrogram Client.
    
    Returns:
        Client: Configured Pyrogram Client instance
    """
    try:
        app = Client(
            name="menfess",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins=dict(root="handlers")
        )
        
        # Register cleanup function
        atexit.register(save_all)
        
        # Validate API credentials
        if not all((API_ID, API_HASH, BOT_TOKEN)):
            raise ValueError("Missing required API credentials in config.py")
            
        return app
        
    except Exception as e:
        logger.error(f"Failed to initialize bot: {str(e)}")
        raise

def main():
    """
    Main entry point for the bot application.
    """
    try:
        app = initialize_bot()
        logger.info("Starting menfess bot...")
        
        # Start the keep_alive and bot
        keep_alive()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    main()
