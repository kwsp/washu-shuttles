#!/bin/sh

# Run crawler to generate JSON data
python3 -m pip install -r requirements.txt
python3 ./crawler.py

# copy json data to frontend public directory
cp ./data.json ./frontend/public/

# build frontend
cd frontend
npm ci
npm run build
