#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request
"""This module provides Main entry point script."""
app = Flask(__name__)
from src.main import main

if __name__ == "__main__":
    main()