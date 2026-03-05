"""Comprehensive demo for PocketLogger features.

Run: python test.py
This script demonstrates console-print capture, stderr capture,
multiline logs, raw writes, toggling settings, and unique filename options.
"""

import sys
import time
from pocket_logger import PocketLogger


def _section(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print()


def demo_basic() -> None:
    _section("Basic logger: console + file timestamps")
    pl = PocketLogger(
        log_file_path="logs/basic_demo",
        print_time=True,
        print_message=True,
        save_time=True,
        save_message=True,
        add_date_and_time_to_log_file_name=True,
        create_new_log_file=True,
    )

    print("A printed message — appears on console and is logged.")
    pl.log("Direct call to pl.log(): hello from PocketLogger")
    pl.log("Multi-line message:\nLine A\nLine B")
    sys.stderr.write("This write to stderr should also be captured.\n")
    pl.restore()
    print("Logger restored — prints no longer forwarded to log file.")


def demo_multiple_loggers() -> None:
    _section("Multiple loggers: prints forwarded to all registered loggers")
    a = PocketLogger(log_file_path="logs/multi_A.log", print_time=True, save_time=True)
    b = PocketLogger(log_file_path="logs/multi_B.log", print_time=True, save_time=True)

    print("Message while both loggers are registered — goes to A and B.")
    a.log("Entry written directly to A")

    # Unregister B and show subsequent prints only go to A
    b.restore()
    print("After restoring B, only logger A receives this print.")
    a.restore()


def demo_toggle_settings() -> None:
    _section("Toggling logger settings at runtime")
    p = PocketLogger(log_file_path="logs/toggle.log", print_time=False, save_time=True)
    print("Console timestamps disabled for this logger.")
    p.log("Saved with timestamp (file_timestamp default True)")

    p.file_timestamp = False
    p.log("Saved without timestamp (file_timestamp=False)")

    p.file_message = False
    p.log("This message will not be written into the file (file_message=False)")
    p.file_message = True
    p.restore()


def demo_raw_write() -> None:
    _section("Raw writes: use log_raw() to append arbitrary content")
    r = PocketLogger(log_file_path="logs/raw_demo.log", print_time=False, save_time=False, save_message=False)
    r.log_raw("RAW: Start of raw log\n")
    r.log_raw("RAW: Another raw line\n")
    r.restore()
    print("Raw content appended to logs/raw_demo.log")


def demo_unique_filenames() -> None:
    _section("Unique filenames and timestamped filenames")
    t1 = PocketLogger(log_file_path="logs/unique.log", add_date_and_time_to_log_file_name=True, create_new_log_file=True)
    t1.log("Logger with date/time appended to filename")

    # Creating another logger pointing to the same base path
    t2 = PocketLogger(log_file_path="logs/unique.log", add_date_and_time_to_log_file_name=False, create_new_log_file=True)
    t2.log("Second logger will get a unique filename to avoid overwrite")

    t1.restore()
    t2.restore()


def main() -> None:
    demo_basic()
    time.sleep(0.05)
    demo_multiple_loggers()
    time.sleep(0.05)
    demo_toggle_settings()
    time.sleep(0.05)
    demo_raw_write()
    time.sleep(0.05)
    demo_unique_filenames()

    print()
    print("Demo complete — inspect the logs/ directory for generated .log files.")


if __name__ == "__main__":
    main()