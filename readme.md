# Freya Assistant

Freya Assistant is a simple voice assistant in Python. It utilizes PocketSphinx for wake word detection, OpenAI for text-to-speech (TTS), and Google Speech API for speech-to-text (STT).

## Requirements

- OpenWeahter Map key: `OPEN_WEATHER_MAP_KEY`
- OpenAI API key: `OPENAI_API_KEY`

## Installation

1. Clone the repository: `git clone https://github.com/your_username/freya-assistant.git`
2. Navigate to the project directory: `cd freya-assistant`
3. Install the dependencies: `pip install -r requirements.txt`

## Usage

1. Set the OpenAI API key as an environment variable: `export OPENAI_API_KEY=your-openai-api-key`
2. Run the assistant: `freya_application.py`

To interact with the Freya Assistant, simply say the wake word "Freya" followed by your command. The assistant will convert your speech to text and then respond using text-to-speech.

## Adding New Skills

Adding new skills to Freya Assistant is easy. Follow these steps:

1. Copy an existing skill folder and give it a new name.
2. Customize the `intents.yaml` file to define the new skill's intents and their corresponding actions.
3. Modify the `__init__.py` file inside the skill folder to implement the desired functionality for the intents.

## Contributing

Contributions are welcome! If you would like to contribute to Freya Assistant, please follow these steps:
 
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push the branch to your forked repository: `git push origin feature/your-feature-name`
5. Open a pull request.

## License

[MIT License](LICENSE)

## Contact

For any questions or feedback, please contact [Andreas Dohren](https://github.com/dohren).

https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/German/
tar -xzvf cmusphinx-de-voxforge-5.2.tar.gz
