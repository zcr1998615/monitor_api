@echo off
chcp 65001 >nul
title Network Traffic Monitor - English Version
cd /d "%~dp0"
python en\monitor.py
pause
