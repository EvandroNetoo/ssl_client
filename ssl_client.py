import threading
from vision_receiver import VisionReceiver
from command_sender import CommandsSender


def main():
    vision_thread = threading.Thread(target=VisionReceiver.run)
    command_thread = threading.Thread(target=CommandsSender.run)

    vision_thread.start()
    command_thread.start()


if __name__ == "__main__":
    main()
