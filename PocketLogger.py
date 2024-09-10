import builtins
import os
import sys
from datetime import datetime

class PocketLogger:
    def __init__(self, log_file_path=None,
                 print_time=True, print_message=True,
                 save_time=True, save_message=True,
                 add_date_and_time_to_log_file_name=False,
                 create_new_log_file=True):
        self.log_file_path = log_file_path
        self.print_time = print_time
        self.print_message = print_message
        self.save_time = save_time
        self.save_message = save_message

        if self.log_file_path:
            if not self.log_file_path.endswith('.log'):
                self.log_file_path += '.log'
            log_dir = os.path.dirname(self.log_file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            if add_date_and_time_to_log_file_name:
                self.log_file_path = self._add_date_and_time_to_log_file_name(self.log_file_path)
            if create_new_log_file:
                self.log_file_path = self._get_new_log_file_path(self.log_file_path)

        self.original_print = builtins.print
        self.original_stderr = sys.stderr
        self.override_print()
        self.override_stderr()

    def override_print(self):
        def custom_print(*args, **kwargs):
            message = ' '.join(map(str, args))
            if self.print_time:
                current_time = self.get_timestamp()
                message = f'[{current_time}] {message}'
            self.original_print(message)  # Print to console
            self.log(message)  # Log to file
        builtins.print = custom_print

    def override_stderr(self):
        class StderrLogger:
            def __init__(self, logger, original_stderr):
                self.logger = logger
                self.original_stderr = original_stderr

            def write(self, message):
                if message.strip():
                    self.logger.log_raw(message)
                self.original_stderr.write(message)

            def flush(self):
                self.original_stderr.flush()

        sys.stderr = StderrLogger(self, self.original_stderr)

    def _get_new_log_file_path(self, path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = f"{base} ({counter}){ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base} ({counter}){ext}"
        return new_path

    def _add_date_and_time_to_log_file_name(self, path):
        base, ext = os.path.splitext(path)
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return f"{base}_{current_time}{ext}"

    def get_time(self) -> str:
        return datetime.now().strftime('%H:%M:%S')

    def get_date(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')

    def get_timestamp(self) -> str:
        return f"{self.get_date()} {self.get_time()}"

    def log(self, message):
        save_parts = []

        if self.save_time:
            current_time = self.get_timestamp()
            save_parts.append(f'[{current_time}]')

        if self.save_message:
            if '\n' in message:
                message = f'\n{message}\n'
            save_parts.append(message)

        save_message = '  '.join(save_parts)

        if self.log_file_path and (self.save_message or self.save_time):
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(save_message + '\n')

    def log_raw(self, message):
        if self.log_file_path:
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(message)
