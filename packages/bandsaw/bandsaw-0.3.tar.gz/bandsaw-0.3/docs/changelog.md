# Changelog

## 0.3: Tracking, metrics and logging

  - New `TrackerExtension` to keep track of workflow runs, executions
    of tasks, their results and attached files.
  - Add new `MetricsAdvice` that gathers metrics when executing tasks
  - Support for file attachments on a session
  - LoggingAdvice adds per-session log file as attachment
  - JsonFormatter for storing log items in a structured format
  - new session id to uniquely identify sessions
  - Fix: Specifying advice chain in @task decorator was broken

## 0.2: Remote execution of tasks

  - Distribute task executions to remote machines via SSH
  - Renamed "Run" which contains arguments for executing a task
    to "Execution"
  - Ability to parameterize task to be used by advices
  - Introduce run id as unique identifier for individual workflow runs

## 0.1: Initial release of the package.

  - Support for free functions as tasks
  - Ability to run tasks in subprocesses
  - Ability to execute tasks with different python interpreters
  - Simple file system cache for caching task results
