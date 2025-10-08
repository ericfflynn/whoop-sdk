# Whoop SDK

A modern Python SDK for the WHOOP Developer API (v2). Easily integrate WHOOP fitness data into your Python applications with simple authentication and intuitive API calls.

## Prerequisites

- Python 3.10 or higher
- A WHOOP developer account and application

## Getting Started

### 1. Create a WHOOP Developer Application

Before using this SDK, you'll need to create a developer application on WHOOP's platform:

1. Visit the [WHOOP Developer Portal](https://developer.whoop.com/)
2. Sign up or log in to your WHOOP account
3. Create a new application
4. Note down your **Client ID** and **Client Secret**
5. Set your redirect URI to `https://www.google.com` (or your preferred redirect URL)

The SDK will request the following scopes:
- `offline` - For refresh token access
- `read:profile` - Read user profile information
- `read:recovery` - Read recovery data
- `read:sleep` - Read sleep data
- `read:workout` - Read workout data

### 2. Installation

Install the SDK from PyPI:

```bash
pip install whoop-sdk
```

### 3. Configuration & Authentication

The SDK supports three ways to provide your credentials:

#### Option 1: Environment Variables (Recommended)
```bash
export WHOOP_CLIENT_ID="your_client_id_here"
export WHOOP_CLIENT_SECRET="your_client_secret_here"
```

#### Option 2: Interactive Setup
If no environment variables are found, the SDK will prompt you for credentials on first run.

#### Option 3: Settings File
Credentials are automatically saved to `~/.whoop_sdk/settings.json` after interactive setup.

### 4. Quick Start

Here's a basic example to get you started:

```python
from whoop_sdk import Whoop

# Initialize the SDK
whoop = Whoop()

# Perform OAuth login (first time only)
whoop.login()

# Your tokens are now saved and ready to use!
```

#### What happens during login:

1. The SDK opens your browser to the WHOOP authorization page
2. You'll be redirected to `https://www.google.com/?code=XXXX&state=whoop_sdk_state_12345`
3. Copy the `code` parameter from the URL and paste it when prompted
4. The SDK exchanges the code for access and refresh tokens
5. Tokens are saved to `~/.whoop_sdk/config.json` for future use

The SDK automatically handles token refresh, so you only need to authenticate once!

## Open Source

This project is open source and welcomes contributions from the community! 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Repository

- **Homepage**: https://github.com/ericfflynn/whoop-sdk
- **Repository**: https://github.com/ericfflynn/whoop-sdk

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Documentation

More detailed documentation and API reference coming soon. For now, check out the source code in the `whoop_sdk` package for available methods and functionality.
