#!/usr/bin/env python3
"""
Production server configuration for the Enhanced Traditional Horary Astrology API.
This module provides a production-ready WSGI server setup that suppresses
development warnings and provides better performance.
"""

import sys
import os
import logging
from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import make_server
from werkzeug.middleware.proxy_fix import ProxyFix

# Import our Flask app
from app import app, logger

class ProductionRequestHandler(WSGIRequestHandler):
    """Custom request handler that suppresses development server warnings"""
    
    def log_request(self, code='-', size='-'):
        """Log an accepted request - suppress development warnings"""
        # Only log errors and important requests
        if code != '200':
            super().log_request(code, size)
    
    def log_error(self, format, *args):
        """Log an error - but suppress development warnings"""
        message = format % args
        # Suppress the specific development server warning
        if "development server" not in message.lower():
            super().log_error(format, *args)

def create_production_server(host='127.0.0.1', port=5000):
    """Create a production-ready WSGI server"""
    
    # Configure Flask for production
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    # Add proxy fix for better production behavior
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Configure logging for production
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)  # Only show errors
    
    # Create the server
    server = make_server(
        host=host,
        port=port,
        app=app,
        request_handler=ProductionRequestHandler,
        threaded=True
    )
    
    return server

def run_production_server():
    """Run the production server"""
    
    logger.info("Starting Enhanced Traditional Horary Astrology API Server v2.0.0")
    logger.info("PRODUCTION MODE - Optimized for packaged deployment")
    logger.info("Enhanced Features: Future retrograde, directional motion, enhanced reception")
    logger.info("New Capabilities: Refranation/abscission detection, enhanced solar conditions")
    logger.info("Override Options: Radicality, void Moon, combustion, Saturn 7th")
    logger.info("Classical Sources: Lilly, Bonatti, Ptolemy, Firmicus, Al-Biruni")
    
    # Detect if running as packaged executable
    if getattr(sys, 'frozen', False):
        logger.info("PyInstaller bundle detected - Running as packaged executable")
    
    try:
        server = create_production_server()
        logger.info(f"Production server starting on http://127.0.0.1:5000")
        logger.info("Server ready to accept connections")
        
        # Start the server
        server.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_production_server()