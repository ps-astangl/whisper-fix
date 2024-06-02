import logging
import warnings

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Ignore UserWarning category warnings
warnings.filterwarnings("ignore", category=UserWarning)
