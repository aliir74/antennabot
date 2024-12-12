# AntenBot - Telegram APN Configuration Bot

A Telegram bot that provides APN configuration files based on user's SIM card provider, with channel subscription verification and optional tutorial links.

## Features

- Provides APN configuration files for different mobile carriers
- Channel subscription verification before file delivery
- Optional YouTube tutorial links with configuration files
- Docker containerization
- Automated deployment via GitHub Actions

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AntenBot.git
cd AntenBot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file from template:
```bash
cp .env.example .env
```

4. Edit `.env` file with your configuration:
- Add your Telegram Bot Token
- Set your channel username/ID
- Configure tutorial links if needed

## Configuration Files

Place your APN configuration files in the `files` directory:
- `files/mci_config.txt`
- `files/irancell_config.txt`
- `files/rightel_config.txt`

## Running Locally

```bash
python bot.py
```

## Docker Deployment

Build and run with Docker:

```bash
docker build -t antenbot .
docker run -d --name antenbot --env-file .env -v $(pwd)/files:/app/files antenbot
```

## GitHub Actions Deployment

To enable automated deployment, set these repository secrets:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password
- `VPS_HOST`: Your VPS IP address
- `VPS_USERNAME`: Your VPS SSH username
- `VPS_SSH_KEY`: Your VPS SSH private key
- `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token
- `TELEGRAM_CHANNEL`: Your Telegram Channel ID/Username
- `ENABLE_TUTORIAL_LINKS`: true/false
- `YOUTUBE_TUTORIAL_LINKS`: Comma-separated tutorial links

## License

MIT License 