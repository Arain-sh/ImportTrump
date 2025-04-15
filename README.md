# Truth Social Monitor

A Python script to monitor new posts by Donald Trump (@realDonaldTrump) on Truth Social and send notifications via IFTTT.

## Features

- Monitors Trump’s Truth Social posts using Apify’s Truth Social Scraper API.
- Sends notifications for new posts via IFTTT Webhooks.
- Logs activity to both console and file (`monitor.log`).
- Configurable polling interval.

## Prerequisites

- Python 3.8 or higher
- Apify account and API token ([Apify](https://apify.com))
- IFTTT account with Webhooks configured ([IFTTT Webhooks](https://ifttt.com/maker_webhooks))

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Arain-sh/ImportTrump.git
   cd ImportTrump
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Copy the example configuration file and fill in your credentials:

   ```
   cp config.example.json config.json
   ```

   Edit config.json with your Apify API token and IFTTT Webhook URL.

## Configuration

The config.json file contains:

- apify_token: Your Apify API token.
- ifttt_webhook_url: Your IFTTT Webhook URL for notifications.
- poll_interval: Polling interval in seconds (default: 300).

Example:

```
{  "apify_token": "your_apify_api_token",  "ifttt_webhook_url": "your_ifttt_webhook_url",  "poll_interval": 300 }
```

## Usage

Run the script:

```
python src/monitor.py
```

The script will:

- Check for new posts every poll_interval seconds.
- Log activity to monitor.log and console.
- Send notifications for new posts via IFTTT.

## Notes

- Ensure config.json is correctly configured before running.
- The script uses Apify’s Truth Social Scraper, which may require a paid plan for heavy usage.
- Logs are saved to monitor.log for debugging.

## License

This project is licensed under the MIT License. See the  file for details.

## Disclaimer

This project is for educational purposes only. Ensure compliance with Truth Social’s [Terms of Service](https://help.truthsocial.com/legal/terms-of-service/) and Apify’s usage policies.
