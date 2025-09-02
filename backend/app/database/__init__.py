# -*- coding: utf-8 -*-
"""
Database package
- Simple and efficient database operations
- Cloud MongoDB support
"""

from .manager import DatabaseManager, db_manager

__all__ = ['DatabaseManager', 'db_manager']