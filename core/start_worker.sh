#!/bin/bash
cd /home/$(whoami)/DarkMatterK3-Home/core
source venv/bin/activate
python t4_worker.py
