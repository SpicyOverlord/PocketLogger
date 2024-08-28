import os
import datetime
import inspect


class PocketLogger:
    def __init__(self, log_file_path=None,
                 print_time=True, print_caller=True, print_message=True,
                 save_time=True, save_caller=True, save_message=True,
                 add_date_and_time_to_log_file_name=False,
                 create_new_log_file=True):
        self.log_file_path = log_file_path
        self.print_time = print_time
        self.print_caller = print_caller
        self.print_message = print_message
        self.save_time = save_time
        self.save_caller = save_caller
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
        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return f"{base}_{current_time}{ext}"

    def get_time(self) -> str:
        return datetime.datetime.now().strftime('%H:%M:%S')

    def get_date(self) -> str:
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def get_timestamp(self) -> str:
        return f"{self.get_date()} {self.get_time()}"

    def log(self, message):
        print_parts = []
        save_parts = []

        if self.print_time or self.save_time:
            current_time = self.get_timestamp()
            if self.print_time:
                print_parts.append(f'[{current_time}]')
            if self.save_time:
                save_parts.append(f'[{current_time}]')

        if self.print_caller or self.save_caller:
            caller_frame = inspect.stack()[1]
            caller_file = os.path.basename(caller_frame.filename)
            caller_function = caller_frame.function
            caller_info = f'{caller_file}.{caller_function}'
            if self.print_caller:
                print_parts.append(caller_info)
            if self.save_caller:
                save_parts.append(caller_info)

        if self.print_message or self.save_message:
            if '\n' in message:
                message = f'\n{message}\n'
            if self.print_message:
                print_parts.append(message)
            if self.save_message:
                save_parts.append(message)

        print_message = '  '.join(print_parts)
        save_message = '  '.join(save_parts)

        if self.print_message or self.print_time or self.print_caller:
            print(print_message)
        if self.log_file_path and (self.save_message or self.save_time or self.save_caller):
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(save_message + '\n')