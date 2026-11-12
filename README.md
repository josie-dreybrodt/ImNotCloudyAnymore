# I'm Not Cloudy Anymore

A small desktop weather widget for Windows, built with Python and PyQt6.
It detects your location via IP geolocation and shows the current weather
as an animated pixel-art sprite in a transparent, frameless window.

<img src="sprite/SunSprite.gif" width="96" alt="Sun"> <img src="sprite/RainSprite.gif" width="96" alt="Rain"> <img src="sprite/SnowSprite.gif" width="96" alt="Snow"> <img src="sprite/NightSprite.gif" width="96" alt="Night">

## Motivation

I wanted to build something small but complete that I would actually use
every day. A weather widget was a good fit: simple enough to finish, but it
still covers real-world topics like working with external APIs, keeping a
GUI responsive with threads and handling network errors. It also let me
combine programming with pixel art: all sprites are drawn by me.

## Features

- Automatic location detection via [ipwho.is](https://ipwho.is/)
- Current weather from the [Open-Meteo API](https://open-meteo.com/)
- Self-drawn pixel-art sprites for sun, clouds, fog, rain, snow, thunderstorms and night
- Network requests run in background threads, so the UI stays responsive
- Automatic refresh every two minutes
- Last successful response is cached in `data.json` and used as a fallback when offline

## Tech Stack

- **Language:** Python 3
- **GUI:** PyQt6
- **Libraries:** requests, python-dotenv (see `requirements.txt`)
- **APIs:** Open-Meteo, ipwho.is

## What I Learned

- Working with REST APIs using `requests` and handling failed requests
- Keeping a GUI responsive by moving network calls into background threads
- Building a custom PyQt6 window: frameless, transparent, with timers and fade animations
- Separating the weather logic (`weather.py`) from the user interface (`UI.py`)
- Caching API responses as JSON to provide an offline fallback
- Keeping local configuration out of version control with `.env` and `.gitignore`
- Creating pixel-art sprites and playing them as GIF animations with `QMovie`

## Project Structure

```
├── UI.py              # Entry point, window and animations (PyQt6)
├── weather.py         # Weather logic: location, API requests, caching
├── sprite/            # Animated GIF sprites
└── requirements.txt
```

## Running the App

1. Clone the repository:

```
git clone https://github.com/josie-dreybrodt/ImNotCloudyAnymore.git
```

2. Install the dependencies with `pip install -r requirements.txt` and create a `.env` file with the endpoints `WEATHER_API_KEY` (Open-Meteo) and `IP_API_KEY` (ipwho.is).

3. Start the widget with `python UI.py`.

## Roadmap

- 7-day forecast
- Smoother animations and transitions between weather states

## About

Portfolio project created during my retraining as an IT Specialist for
Application Development (Fachinformatikerin für Anwendungsentwicklung).
