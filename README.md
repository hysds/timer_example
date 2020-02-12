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
[2020-02-12 08:14:39,706: ERROR/evaluator_with_timer/main] [Errno 2] No such file or directory: 'test_dir'

# test timer expiration
$ mkdir test_dir
$ ./evaluator_with_timer.py test_dir 2 --max_time=10
[2020-02-12 08:17:30,361: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:17:30,361: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:17:30,361: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.6s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:17:31,006: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:17:31,006: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:17:31,007: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.7s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:17:31,756: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:17:31,757: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:17:31,757: INFO/backoff/_log_backoff] Backing off evaluate(...) for 2.5s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:17:34,274: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:17:34,274: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:17:34,275: INFO/backoff/_log_backoff] Backing off evaluate(...) for 4.2s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:17:38,462: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:17:38,462: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:17:38,463: INFO/backoff/_log_backoff] Backing off evaluate(...) for 1.9s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:17:40,367: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:17:40,367: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:17:40,368: ERROR/backoff/_log_giveup] Giving up evaluate(...) after 6 tries (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:17:40,368: ERROR/evaluator_with_timer/main] Conditions not met.

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
[2020-02-12 08:18:52,923: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:18:52,923: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:18:52,924: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.1s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:18:53,018: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:18:53,019: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:18:53,020: INFO/backoff/_log_backoff] Backing off evaluate(...) for 1.1s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:18:54,132: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:18:54,132: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:18:54,134: INFO/backoff/_log_backoff] Backing off evaluate(...) for 0.7s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:18:54,873: INFO/evaluator_with_timer/check_condition] found: 0
[2020-02-12 08:18:54,873: INFO/evaluator_with_timer/check_condition] files: []
[2020-02-12 08:18:54,874: INFO/backoff/_log_backoff] Backing off evaluate(...) for 8.0s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:19:02,872: INFO/evaluator_with_timer/check_condition] found: 1
[2020-02-12 08:19:02,872: INFO/evaluator_with_timer/check_condition] files: ['test1']
[2020-02-12 08:19:02,873: INFO/backoff/_log_backoff] Backing off evaluate(...) for 12.0s (ConditionNotMetError: Conditions not met.)
[2020-02-12 08:19:14,925: INFO/evaluator_with_timer/check_condition] found: 2
[2020-02-12 08:19:14,925: INFO/evaluator_with_timer/check_condition] files: ['test1', 'test2']
[2020-02-12 08:19:14,926: INFO/evaluator_with_timer/evaluate] Conditions met.

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
