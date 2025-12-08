#!/usr/bin/env python3
"""
Production Server for NtandoComputer
Optimized for Render.com deployment
"""

import os
import sys
from computer import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)