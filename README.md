<p align="center"><img src="https://www.vesperbot.ai/images/icon.png" width="105" /></p>

# Vesper &middot; [vesperbot.ai]([https://www.vesperbot.ai/](https://vesperbot.ai/))

Vesper is an agentic AI Discord bot.

## Purpose
Vesper can manage just about any aspect of your server. From moderation to server customisation, Vesper makes the perfect moderator or administrator. As for how to use Vesper, simply ask it to do something (examples: 'Give me the Green role', 'Create a channel called gaming and make it private to the gaming role'), and it will oblige.

## Setup
If you wish to run Vesper yourself, follow the instructions below.

> Note: Python 3.12 is the recommended Python version for running Vesper

### 1. Create a .env file in the root of the repository
Follow the structure provided below, with your own credentials.
```
TOKEN=
APPLICATION_ID=
EMBED_COLOR=

OPENAI_API_KEY=
GOOGLE_API_KEY=
XAI_API_KEY=

SUPABASE_URL=
SUPABASE_KEY=
```

### 2. Create & enter a virtual environment
Run the command `python3 -m venv .venv` and then either `source .venv/bin/activate` or `.venv/Scripts/activate` for Windows.

### 3. Install dependencies
Once inside the virtual environment, run the command `pip install -r requirements.txt`.

### 4. Running Vesper
Once you have completed the above, run `python src/vesper.py` from the project root to start.

Thank you for using Vesper! Please consider donating by [clicking here](https://www.vesperbot.ai/donate).

&ndash; [Harvey Coombs](https://www.harveycoombs.com/)
