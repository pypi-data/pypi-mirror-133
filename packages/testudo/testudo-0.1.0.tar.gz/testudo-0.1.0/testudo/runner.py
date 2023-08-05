from pathlib import Path
from shlex import split
from subprocess import STDOUT, Popen, PIPE
from threading import Event
from typing import List, Optional, Generator

from typeguard import typechecked

from testudo.config import TaskConfig
from testudo.log import log
from testudo.reporter import start_reporter_daemon
from testudo.task_manager import task_manager

@typechecked
def report_failure(db: Path, task_id: str, output: str, exit_code: int, stack_trace: Optional[str] = None) -> None:
    with task_manager(db) as tm:
        tm.report_failure(task_id, output, exit_code, stack_trace)


@typechecked
def report_success(db: Path, task_id: str, output: str) -> None:
    with task_manager(db) as tm:
        tm.report_success(task_id, output)

@typechecked
def run(db: Path, task_id: str, cmd: List[str]) -> bool:
    log.info(f"Running Task [{task_id}]...")
    with Popen(cmd, stderr=STDOUT, stdout=PIPE) as proc:
        output = []
        while proc.poll() is None:
            if proc.stdout is not None:  # pragma: no branch
                if line := proc.stdout.readline():
                    log.info(f'[{task_id}] OUTPUT: {line.decode().rstrip()}')
                    output.append(line.decode().rstrip())
        exit_code = proc.returncode
        if exit_code == 0:
            log.info(f"Task [{task_id}] successful!")
            report_success(db, task_id, '\n'.join(output))
            return True
        log.warning(f"Task [{task_id}] failed!")
        report_failure(db, task_id, '\n'.join(output), exit_code)
        return False

@typechecked
def run_with_delay(db: Path, task_id: str,
                   cmd: List[str],
                   delay_seconds: float,
                   halt_flag: Event,
                   on_failure_delay_seconds: Optional[float] = None) -> Generator[bool, None, None]:
    on_failure_delay_seconds = on_failure_delay_seconds or delay_seconds
    while 42:
        success = run(db, task_id, cmd)
        yield success
        if halt_flag.wait(delay_seconds if success else on_failure_delay_seconds):
            break

@typechecked
def run_with_reporter(db: Path, config: TaskConfig, halt: Optional[Event] = None) -> None:
    first_run_complete = False
    _halt = halt or Event()
    for _ in run_with_delay(db, config.task_id, split(config.command),
                            delay_seconds=config.delay_seconds, halt_flag=_halt,
                            on_failure_delay_seconds=config.on_failure_delay_seconds):
        if not first_run_complete:
            first_run_complete = True
            start_reporter_daemon(db, config, halt=_halt)
