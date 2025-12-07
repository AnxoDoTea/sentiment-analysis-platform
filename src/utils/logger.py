import os
import sys
import logging

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger with the specified name and configuration based on environment variables.
    
    Environment Variables:
    - LOG_LEVEL: Sets the logging level (default: INFO)
    - DEBUG_MODE: If 'true', overrides LOG_LEVEL to DEBUG (default: false)
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    if debug_mode:
        log_level = "DEBUG"
        
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    return logging.getLogger(name)
