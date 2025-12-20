import fal_client
from dotenv import load_dotenv

load_dotenv()

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])

def text_to_speech(text, speaker="Carter"):
    result = fal_client.subscribe(
        "fal-ai/vibevoice/0.5b",
        arguments={
            "script": text,
            "speaker": speaker
        },
        with_logs=True,
        on_queue_update=on_queue_update
    )

    return result