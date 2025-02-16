import time
from RealtimeSTT import AudioToTextRecorder
from pynput import keyboard
import pyperclip
from pynput.keyboard import Key, Controller

class SpeechTyper:
    def __init__(self):
        self.recorder = AudioToTextRecorder(realtime_model_type="medium", model="medium")
        self.transcribed_text = ""
        self.keyboard_controller = Controller()
        self.previous_clipboard = None

        # Double-click detection variables
        self.last_ctrl_press_time = 0
        self.last_ctrl_release_time = 0
        self.DOUBLE_CLICK_TIME = 0.3  # Maximum time between clicks (seconds)
        self.MAX_HOLD_TIME = 0.2      # Maximum time key can be held to count as a click


    def save_clipboard(self):
        """Save current clipboard content"""
        try:
            self.previous_clipboard = pyperclip.paste()
        except:
            self.previous_clipboard = ""

    def restore_clipboard(self):
        """Restore previous clipboard content"""
        if self.previous_clipboard is not None:
            try:
                pyperclip.copy(self.previous_clipboard)
            except:
                pass
            self.previous_clipboard = None

    def on_press(self, key):
        if key == Key.ctrl_l:  # Left control press
            current_time = time.time()
            self.last_ctrl_press_time = current_time

    def on_release(self, key):
        if key == Key.ctrl_l:  # Left control release
            current_time = time.time()
            hold_duration = current_time - self.last_ctrl_press_time
            time_since_last_release = current_time - self.last_ctrl_release_time

            # Check if this was a quick press (not held down) and if it's the second click
            if (hold_duration < self.MAX_HOLD_TIME and
                time_since_last_release < self.DOUBLE_CLICK_TIME and
                self.last_ctrl_release_time != 0):
                self.listen()
                # Reset release time to prevent triple-click detection
                self.last_ctrl_release_time = 0
            else:
                # Update last release time for the first click
                self.last_ctrl_release_time = current_time

    def listen(self):
        # if hasattr(key, 'name') and key.name == 'ctrl_r':
            print("Started listening. Speak now...")
            self.recorder.text(self.process_text)
            self.recorder.stop()
            time.sleep(0.1)
            print("Stopped listening.")
            self.insert_text()

    def process_text(self, text):
        self.transcribed_text += text + " "
        print(f"Transcribed: {text}")

    def insert_text(self):
        if self.transcribed_text:
            print(f"Preparing to insert text: {self.transcribed_text}")
            self.save_clipboard()

            try:
                # Copy the transcribed text to clipboard
                pyperclip.copy(self.transcribed_text)
                time.sleep(0.1)  # Give the clipboard a moment to update

                # Verify the clipboard contains our text
                current_clipboard = pyperclip.paste()
                print(f"Clipboard content before paste: {current_clipboard[:50]}...")

                # Perform the paste operation
                time.sleep(0.1)  # Small delay before paste
                self.keyboard_controller.press(Key.ctrl)
                time.sleep(0.05)  # Small delay after ctrl press
                self.keyboard_controller.press('v')
                time.sleep(0.05)  # Small delay before releasing
                self.keyboard_controller.release('v')
                self.keyboard_controller.release(Key.ctrl)
                time.sleep(0.1)  # Small delay after paste

            except Exception as e:
                print(f"Error during paste operation: {e}")

            finally:
                # Restore previous clipboard content
                time.sleep(0.1)  # Give the paste operation time to complete
                self.restore_clipboard()
                self.transcribed_text = ""

    def run(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            listener.join()

if __name__ == '__main__':
    typer = SpeechTyper()
    typer.run()