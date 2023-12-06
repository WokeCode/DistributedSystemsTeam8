import os
import time 
class Logger():
    LogFunc = None
    def __init__(self, name):
        self.startTime = time.time()
        self.name = name
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, 'logs', f'pod{self.name}.txt')

        if os.path.exists(self.file_path):  # Check if the file exists
            os.remove(self.file_path)      # Delete the existing file

        # Create a new file with the same name
        with open(self.file_path, 'a') as new_file:
            new_file.write(f"Started Logging to {self.name}\n")

    def Log(self, content):
        print(content)
        with open(self.file_path, 'a') as file:
            string = f"{self.name}: {content} "
            #spaces = (100 - len(string))*" "
            the_time = int(time.time()-self.startTime)
            time_string = "" #f"{spaces}Time: {the_time}"
            file.write(f"Pod{self.name} ({the_time}s): {content} {time_string}\n")
