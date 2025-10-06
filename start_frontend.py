#!/usr/bin/env python3
"""
Frontend server startup script
"""
import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "frontend_server:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="info"
    )
