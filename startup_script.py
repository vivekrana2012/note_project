import sys
import logging
from datetime import datetime
from rss_puller import pull

# Configure logging
log_filename = f"logs/rss_pull_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for RSS puller script
    Suitable for running via cron or scheduler
    """
    try:
        logger.info("="*80)
        logger.info("Starting RSS Pull Job")
        logger.info("="*80)
        
        # Run the pull flow
        pull()
        
        logger.info("="*80)
        logger.info("RSS Pull Job Completed Successfully")
        logger.info("="*80)
        
        return 0
        
    except Exception as e:
        logger.error(f"RSS Pull Job Failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
