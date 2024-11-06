import asyncio
import os

async def watch_file(filepath, interval=5):
    """Asynchronously checks if a file has changed based on its modification time."""
    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist.")
        return

    # Get the initial modification time
    last_mod_time = os.path.getmtime(filepath)
    print(f"Watching file: {filepath}")

    while True:
        await asyncio.sleep(interval)  # Non-blocking sleep for the specified interval

        # Get the current modification time
        current_mod_time = os.path.getmtime(filepath)

        # Check if the file modification time has changed
        if current_mod_time != last_mod_time:
            print(f"File '{filepath}' has been modified.")
            last_mod_time = current_mod_time
        else:
            print(f"No changes in '{filepath}'")

# Example of another async function that could coexist with the file-watching coroutine
async def other_async_routine():
    while True:
        await asyncio.sleep(3)
        print("Running another asynchronous task.")

# Main entry point to run both async functions concurrently
async def main():
    filepath = "../test.drawio"  # Replace with the path to your file
    await asyncio.gather(
        watch_file(filepath, interval=5),
        other_async_routine(),
    )

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
