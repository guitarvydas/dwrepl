In Python's `asyncio` library, `asyncio.gather` is a function that allows you to run multiple asynchronous tasks concurrently. It is commonly used when you have multiple `async` functions that you want to run at the same time within an event loop, without blocking each other.

### How `asyncio.gather` Works

`asyncio.gather` accepts multiple awaitable objects (like `async` functions or coroutines) as arguments and schedules them to run concurrently. It returns a single future, which will complete when all of the provided tasks have finished.

#### Basic Syntax

```python
asyncio.gather(task1, task2, task3, ...)
```

Each `task` here can be an `async` function or a coroutine. `asyncio.gather` will run each task concurrently and wait until all tasks are completed.

### Example Usage

```python
import asyncio

async def task1():
    await asyncio.sleep(2)
    print("Task 1 completed")
    return "Result from task 1"

async def task2():
    await asyncio.sleep(1)
    print("Task 2 completed")
    return "Result from task 2"

async def task3():
    await asyncio.sleep(3)
    print("Task 3 completed")
    return "Result from task 3"

async def main():
    results = await asyncio.gather(task1(), task2(), task3())
    print("All tasks completed")
    print("Results:", results)

# Run the main function
asyncio.run(main())
```

### Explanation

- **Concurrent Execution**: `task1`, `task2`, and `task3` start at the same time, even though they each have different sleep times. `asyncio.gather` schedules them to run concurrently, so they don't block each other.
- **Order of Completion**: The tasks complete based on their sleep durations:
  - `task2` completes first (1 second).
  - `task1` completes second (2 seconds).
  - `task3` completes last (3 seconds).
- **Results**: The `results` list contains the return values from each task, in the order they were passed to `asyncio.gather`, not based on the order they completed. This would print:
  ```python
  All tasks completed
  Results: ['Result from task 1', 'Result from task 2', 'Result from task 3']
  ```

### Key Points of `asyncio.gather`

1. **Concurrency**: `asyncio.gather` allows asynchronous functions to run concurrently within the same event loop. This is useful for tasks that don’t depend on each other and can run at the same time.

2. **Order of Results**: The results are returned in the same order as the tasks were passed to `gather`, not the order in which they complete.

3. **Error Handling**: If any task raises an exception, `asyncio.gather` will raise an exception immediately, but only once all tasks are done. If `return_exceptions=True` is used, exceptions are returned as part of the results list instead of halting the execution.

    ```python
    results = await asyncio.gather(task1(), task2(), task3(), return_exceptions=True)
    ```

4. **Cancelling Tasks**: Cancelling the gather task will cancel all the tasks that were being awaited within it.

### Practical Use Cases

- **Running I/O Bound Tasks**: Perfect for tasks like reading/writing files, making network requests, or interacting with databases asynchronously.
- **Independent Async Functions**: Good for executing independent `async` functions concurrently without blocking each other, like sending multiple API requests simultaneously.
  
### Summary

`asyncio.gather` is a powerful tool for running multiple `async` functions concurrently within the same event loop, allowing Python code to handle tasks in parallel efficiently. It waits for all tasks to complete, returns their results in order, and handles exceptions gracefully when configured.
