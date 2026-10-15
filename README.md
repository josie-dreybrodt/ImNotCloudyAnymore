# I'm Not Cloudy Anymore ☀️

A lightweight desktop weather widget built with **Python** and **PyQt6**. It detects the user's location automatically and displays the current weather with animated pixel-art sprites in a transparent, frameless window.

<img src="sprite/CloudSprite.gif" width="120" alt="Cloudy"> <img src="sprite/RainSprite.gif" width="120" alt="Rain"> <img src="sprite/SnowSprite.gif" width="120" alt="Snow">

<img src="sprite/NightSprite.gif" width="120" alt="Night"> <img src="sprite/FogSprite.gif" width="120" alt="Fog">

## Motivation

I wanted to build something small but complete that I would actually use every day, instead of another exercise that ends up in a forgotten folder. A weather widget turned out to be the perfect fit: it's simple enough to finish, yet it covers many real-world topics such as working with external APIs, keeping a GUI responsive with threads, and handling errors when the network is unavailable.

I also love pixel art, so this project was a chance to combine my creative side with programming. Drawing the sprites myself and bringing them to life in the app made the learning process much more fun, and it's the first project I'm proud enough of to put in my portfolio.

## Overview

| | |
|---|---|
| **Type** | Desktop application (Windows) |
| **Language** | Python 3 |
| **GUI Framework** | PyQt6 |
| **APIs** | Open-Meteo (weather), IP geolocation |
| **Status** | Working, actively improved |

## Features

- **Automatic location detection** via IP geolocation, no manual input needed
- **Live weather data** from the [Open-Meteo API](https://open-meteo.com/)
- **Animated pixel-art sprites** for sun, clouds, fog, rain, snow, thunderstorms and night
- **Transparent, frameless window** that sits unobtrusively on the desktop
- **Non-blocking updates** using background threads, so the UI stays responsive
- **Automatic refresh** at regular intervals using `QTimer`
- **Offline fallback**: the last successful response is cached locally and shown if the API is unreachable

## Skills Demonstrated

- **REST API integration** with `requests`, including timeouts and error handling
- **Multithreading** to separate network requests from the GUI thread
- **GUI development** with PyQt6 (custom window flags, transparency, animations)
- **Object-oriented design**, with weather logic separated from the user interface
- **Data persistence** using JSON for caching
- **Secure configuration**: API endpoints and keys are stored in environment variables (`.env`) and kept out of version control
- **Error handling and fallbacks** for missing files and failed network requests

## Project Structure

```
ImNotCloudyAnymore/
├── Main.py            # Entry point and GUI
├── weather.py         # API requests, caching and weather-code mapping
├── sprite/            # Animated GIF sprites
├── requirements.txt   # Python dependencies
└── .env               # Local configuration (not included in the repo)
```

## Getting Started

**Requirements:** Python 3 on Windows

```bash
# Clone the repository
git clone https://github.com/josie-dreybrodt/ImNotCloudyAnymore.git
cd ImNotCloudyAnymore

# Create and activate a virtual environment
py -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```
WEATHER_API_KEY=https://api.open-meteo.com/v1/forecast
IP_API_KEY=<IP geolocation API URL>
```

Run the app:

```bash
python Main.py
```

## Roadmap

- Rebuild in **Godot with C#** featuring smoother animations and transitions
- **7-day forecast**

## About Me

I'm currently retraining as an **IT Specialist for Application Development** (Fachinformatikerin für Anwendungsentwicklung). This project is part of my portfolio and reflects my interest in combining clean code with creative, pixel-art visuals.
