# Python Parallel Task Performance Tester

A testing framework for evaluating performance scaling of different computational tasks when parallelized in Python.


## Overview

The intent of this project is to provide a tangible way of understanding the performance scaling of parallel processing in Python and how it depends on the task at hand. It could also be used as a reference point for building a foundation on how much parallelization one might want for a given task and resource constraints. For example, if you have a 4-core cloud instance, would it be best to have 2-4 parallel workers for your application, or no parallelization at all?

In a mixed workload of randomized tasks, my own testing resulted in a 5.9x average speedup (12 workers) at best when compared to running the same tasks sequentially. Best results for a single task type were 9.8x with 16 workers (password hashing & checking) while worst were a slowdown to 0.45x with 16 workers (image manipulation with OpenCV). Tests were run on a system with 12 performance and 4 efficiency CPU cores.


## Features

- Multiple task types:
  - Computationally intensive tasks
  - I/O intensive tasks
  - Memory intensive tasks
  - Fork and add your own or propose some!
- Configurable test parameters (JSON):
  - Number of worker processes (0-n) [0 = direct sequential function calls]
  - Task count
  - Task-specific parameters
  - Test iterations
- Performance metrics:
  - Initialization time
  - Average per task execution time
  - Total task execution time
  - Total runtime (init, work, cleanup)
- CSV export of results


## Installation

```sh
# Clone the repository
git clone https://github.com/daeteria/python-parallel-perf-tester.git
cd parallel-performance-tester

# Install dependencies
pip install -r requirements.txt
```


## Usage

```sh
python main.py --config example_configs/sum.json
```


A valid configuration file is as follows:

```json
{
    "iterations": 10,
    "task": "sort",
    "task_args": [1000000],
    "task_count": 100,
    "workers": [0, 1, 2, 4, 6, 8, 10, 12, 16],
    "wait_time_after_runner": 2.0,
    "wait_time_after_iteration": 2.0,
    "gc_after_iteration": true
}
```

Where
- `iterations`: How many test passes to perform per worker configuration. The output will be an average of all passes.
- `task`: Which task to run. Refer to the Task types section below for more.
- `task_args`: A list of arguments to pass to the task function. Check the `task_func` mapping in `main.py` to see what is the reffered function and what arguments it takes in from the function implementation. All tasks are defined in the `work` module.
- `task_count`: How many tasks to perform per test pass, e.g. how many times the task function gets called in total.
- `workers`: A list of worker configurations to test. 0 here means sequential and is a good reference point to use. 1 means that you have a single parallel process that gets fed tasks by the main process, so basically "sequential with scheduling overhead". It is adviced to at maximum have your system's CPU core count of workers. You can of course try higher numbers, but this can lead to crashing.
- `wait_time_after_runner`: How long to wait after each runner pipeline in seconds, e.g. between running the pipeline for 2 and then 4 workers. Can be used as a cooldown period for your CPU, so that the runs won't affect each other.
- `wait_time_after_iteration`: How long to wait after each test iteration loop in seconds. Can be used as a cooldown period and a reset for your CPU between iterations, so that the iterations won't affect each other.
- `gc_after_iteration`: Whether or not to run garbage collection after each test iteration.

Refer to the example configurations in `example_configs` for more configurations.


## Task types

- `sum`: Integer addition loop [computation]
- `multi`: Floating point multiplication loop [computation]
- `io`: File read/write/delete operations [drive access]
- `zip`: File compression/decompression [computation / drive access]
- `tensor`: Tensor dot product calculation [computation, internally parallelized (Numpy)]
- `sort`: Array sorting [memory-intensive]
- `matrix`: Matrix inversion [memory-intensive]
- `img`: Image manipulation [computation, internally parallelized (OpenCV)]
- `password`: Password hashing and checking [computation]
- `random`: Random mix of above tasks


## Results

Running the application will output a CSV file into `results` directory with averaged runtime details of each configured worker count.

```csv
Name,Workers,Job details,Job count,Time: init,Time: work,Time: task avg,Time: total
sequential,0,1000000,100,0.0,3.3860135316848754,0.033860135316848755,3.3860135316848754
parallel_1,1,1000000,100,0.07361857891082764,4.066215181350708,0.03309207940101623,4.157250261306762
parallel_2,2,1000000,100,0.07397744655609131,2.1326904296875,0.03431025624275207,2.225041055679321
parallel_4,4,1000000,100,0.07331948280334473,1.1610297918319703,0.036153562307357785,1.2573521614074707
parallel_6,6,1000000,100,0.08625915050506591,0.8970386981964111,0.03604542422294617,1.0097821712493897
parallel_8,8,1000000,100,0.0874253273010254,0.913476037979126,0.03618656921386719,1.030402421951294
parallel_10,10,1000000,100,0.0858471155166626,0.9384187698364258,0.03635503387451172,1.054057788848877
parallel_12,12,1000000,100,0.0788438081741333,0.9550837278366089,0.03675771951675415,1.0659477710723877
parallel_16,16,1000000,100,0.08189177513122559,1.0003268718719482,0.03797887063026428,1.1175617694854736
```

## Requirements

- Python 3.x (tested with 3.9.x)
- Python libraries listed in `requirements.txt`


## Credits

Test image from [Unsplash](https://unsplash.com/photos/brown-and-black-snake-on-ground-vec5yfUvCGs)
