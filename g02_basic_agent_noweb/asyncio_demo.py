import asyncio

async def task_with_delay(name, delay):
    print(f"Task {name} started (waiting for {delay} seconds)")
    await asyncio.sleep(delay) # Pauses this task, allows other tasks to run
    print(f"Task {name} finished")
    return f"Result of {name}"

async def main():
    # Create tasks to run concurrently
    task1 = asyncio.create_task(task_with_delay("One", 6))
    task2 = asyncio.create_task(task_with_delay("Two", 3))

    # Await the results
    result1 = await task1
    result2 = await task2
    print(f"Got results: {result1}, {result2}")

# Run the main async function
asyncio.run(main())
