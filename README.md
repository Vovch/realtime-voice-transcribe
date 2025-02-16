# Realtime Speech-to-Text Typing Application

This application allows you to convert speech to text in real-time and automatically type the transcribed text at your cursor position using a simple keyboard shortcut.

## Prerequisites

- Python 3.10.6 (recommended)
- Virtual environment (recommended)

## Features
- Real-time speech recognition using RealtimeSTT
- Double-click left control key to start/stop listening
- Automatic text insertion at cursor position
- Clipboard preservation during text insertion

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/RealtimeSTTTestApp.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. To start dictating:
   - Double-click the left control key (Ctrl)
   - Speak clearly into your microphone
   - The transcribed text will be automatically typed at your cursor position

3. To stop dictating:
   - Double-click the left control key again

## Dependencies
- RealtimeSTT
- pynput
- pyperclip

## License
MIT