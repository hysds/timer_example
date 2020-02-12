# Example of an evaluator job with a timer

## Usage Example

Two examples: one showing the timer expiring because conditions were not met
and a second one showing the conditions being met. In both cases, state config
JSON file is created.

### Timer Expiration
```
$ cd timer_example

# check that exceptions other than ConditionNotMetError are immediately raised
$ ./evaluator_with_timer.py test_dir 2 --max_time=10
Traceback (most recent call last):
  File "./evaluator_with_timer.py", line 100, in <module>
    main(args.path, args.count)
  File "./evaluator_with_timer.py", line 83, in main
    evaluate(path, count)
  File "/Users/gmanipon/anaconda3/lib/python3.7/site-packages/backoff/_sync.py", line 94, in retry
    ret = target(*args, **kwargs)
  File "./evaluator_with_timer.py", line 73, in evaluate
    if check_condition(path, count):
  File "./evaluator_with_timer.py", line 49, in check_condition
    files = os.listdir(path)
FileNotFoundError: [Errno 2] No such file or directory: 'test_dir'

# echo exit status
$ echo $?
1

# test timer expiration
$ mkdir test_dir
$ ./evaluator_with_timer.py test_dir 2 --max_time=10
[2020-02-12 08:33:31,819: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:33:31,819: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:33:31,819: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.3s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:33:32,156: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:33:32,157: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:33:32,158: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.3s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:33:32,419: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:33:32,419: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:33:32,420: INFO/backoff/_log_backoff] Backing off evaluate(...) for 2.5s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:33:34,938: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:33:34,938: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:33:34,939: INFO/backoff/_log_backoff] Backing off evaluate(...) for 2.2s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:33:37,134: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:33:37,134: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:33:37,135: INFO/backoff/_log_backoff] Backing off evaluate(...) for 4.7s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:33:41,822: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:33:41,822: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:33:41,824: ERROR/backoff/_log_giveup] Giving up evaluate(...) after 6 tries (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:33:41,824: ERROR/evaluator_with_timer/main] Conditions not met.
[2020-02-12 08:33:41,824: ERROR/evaluator_with_timer/main] Continuing on without non-zero exit code.

# echo exit status
$ echo $?
0

# contents of the state config
$ cat state_config.json 
{
  "files": [],
  "success": false
}
```

### Conditions Met
In one terminal:
```
$ ./evaluator_with_timer.py test_dir 2
```

In a second terminal:
```
$ cd timer_example/test_dir
$ touch test1
$ touch test2
```

The first terminal should show similar output:
```
$ ./evaluator_with_timer.py test_dir 2
[2020-02-12 08:34:35,135: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:34:35,135: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:34:35,135: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.5s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:34:35,638: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:34:35,638: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:34:35,639: INFO/backoff/_log_backoff] Backing off evaluate(...) for 1.2s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:34:36,868: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:34:36,869: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:34:36,870: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.6s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:34:37,461: INFO/evaluator_with_timer/check_condition] found: 1
[2020-02-12 08:34:37,461: INFO/evaluator_with_timer/check_condition] files: ['test1']
[2020-02-12 08:34:37,462: INFO/backoff/_log_backoff] Backing off evaluate(...) for 1.3s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:34:38,804: INFO/evaluator_with_timer/check_condition] found: 1
[2020-02-12 08:34:38,804: INFO/evaluator_with_timer/check_condition] files: ['test1']
[2020-02-12 08:34:38,805: INFO/backoff/_log_backoff] Backing off evaluate(...) for 7.1s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:34:45,918: INFO/evaluator_with_timer/check_condition] found: 2
[2020-02-12 08:34:45,919: INFO/evaluator_with_timer/check_condition] files: ['test1', 'test2']
[2020-02-12 08:34:45,920: INFO/evaluator_with_timer/evaluate] Conditions met.

# echo exit status
$ echo $?
0

# contents of the state config
$ cat state_config.json 
{
  "files": [
    "test1",
    "test2"
  ],
  "success": true
}
```
