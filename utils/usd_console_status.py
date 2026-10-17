import sys
import threading

def usd_animate_progress_status(
    message: str,
    usd_stop_event: threading.Event
):

    frames = [
        "   ",
        ".  ",
        ".. ",
        "..."
    ]

    index = 0

    while not usd_stop_event.wait(0.5):

        current_message = (
            f"{message}{frames[index]}"
        )

        # Return to beginning of the line
        # and overwrite the previous frame.
        sys.stdout.write(
            f"\r{current_message}"
        )

        sys.stdout.flush()

        index = (
            index + 1
        ) % len(frames)

    # Finish the animation on a clean line.
    sys.stdout.write(
        f"\r{message}...   \n"
    )

    sys.stdout.flush()