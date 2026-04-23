@echo off
chcp 65001 >nul
title 网络流量监控工具 - 中文版
cd /d "%~dp0"
python zh\monitor.py
pause
