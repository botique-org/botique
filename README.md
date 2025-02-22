# Botique - AI Agent Bot Boutique

Botique is a project we started out of our shared interest in building and sharing AI agent bots. While it’s not a fully mature framework yet, it brings together some useful examples and common components—like standardized I/O and deployment helpers—that you can use as building blocks for your own AI-powered bots.

We noticed that finding and keeping useful AI agent bots can be a challenge. Many bots either end up abandoned or aren’t leveraging AI effectively. With Botique, our goal is to create a community space where developers can share their AI agent bot examples, learn from each other’s components, and gradually build up a set of common tools to make development easier.

Feel free to use, modify, and share this project as you see fit.

> **Note:** Botique is released under the MIT License. This license allows any use—including commercial use, modification, distribution, and private use—without additional licensing fees.

## Features

- **Modular Architecture:**  
  Easily add new bot types without modifying the core code.
- **Plugin Registry:**  
  Dynamically load and register bot implementations.
- **Multi-Platform Support:**  
  Deploy bots on Telegram or Discord using dedicated platform wrappers.
- **Configurable via YAML:**  
  Load bot configurations from YAML files for flexibility and ease of customization.
- **Decoupled Dependencies:**  
  Each bot can handle its own external dependencies, allowing for a scalable, lightweight core.

## Installation

1. **Fork & Clone the repository:**

 ```bash
     git clone https://github.com/yourusername/botique.git
     cd botique
 ```
   
2. **Set up a virtual environment (optional but recommended):**
```
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install required dependencies:**
```
    pip install -r requirements.txt
```
## Usage

Once installed, you can run different bots on different platforms using command-line arguments. 

Please check individual READMEs under bots/ for more detailed usage and examples, here's a quick example for Persona bot. 

### Running Bot on Telegram 

```bash
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
python main.py --platform telegram --bot persona --bot_token YOUR_TELEGRAM_BOT_TOKEN
```

### Running Bot on Discord

```bash
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
python main.py --platform discord --bot persona --bot_token YOUR_DISCORD_BOT_TOKEN
```

### Available Command-Line Arguments

| Argument       | Description                                        | Default       |
|-----------------|----------------------------------------------------|--------------|
| `--platform`    | The platform to deploy the bot on (`telegram` or `discord`). | N/A  |
| `--bot`         | The bot type to use (`persona`, `search`, etc.).   | N/A  |
| `--bot_token`   | The bot's authentication token (required).        | N/A         |
| `--config`      | Path to the YAML configuration file.             | `bots/{bot_type}/config.yaml` |

## Contributing

Contributions are welcome! If you'd like to help improve Botique, follow these guidelines:

### Code Contributions

- Ensure new bot types register themselves using the plugin system.
- Maintain code readability and follow best practices.
- Test your changes before submitting a pull request.
- Update documentation if necessary.

### Feature Requests & Bug Reports

- If you have a feature request or found a bug, open an issue on GitHub.
- Provide a clear description and, if applicable, steps to reproduce the issue.
- Suggestions for improvements are always welcome.

### Documentation

- If you improve documentation, ensure it remains clear and concise.
- Contributions to the README, configuration examples, or guides are appreciated.

---

## License

Botique is released under the **MIT License**. You are free to use, modify, and distribute the code for both personal and commercial purposes. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or contributions, please open an issue on GitHub or join our [Discord](https://discord.gg/NKKRQUcRA4). 
