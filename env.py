import subprocess
import sys
import os
import pandas as pd

class EnvironmentSetup:
    def __init__(self, environment_name='env'):
        self.environment_name = environment_name
        self.env_path = os.path.join(os.getcwd(), self.environment_name)
    
    def environment_exists(self):
        # Check if the virtual environment already exists
        return os.path.exists(self.env_path)
    
    def create_environment(self):
        if not self.environment_exists():
            # Create virtual environment
            subprocess.check_call([sys.executable, '-m', 'venv', self.environment_name])
            print(f"Virtual environment '{self.environment_name}' created.")
        else:
            print(f"Virtual environment '{self.environment_name}' already exists.")
    
    def install_libraries(self):
        if self.environment_exists():
            # List of necessary libraries
            libraries = ['openai', 'pandas', 'matplotlib', 'numpy', 'scikit-learn']
            
            # Install each library using pip
            for lib in libraries:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
                print(f"Library '{lib}' installed.")
        else:
            print(f"Virtual environment '{self.environment_name}' does not exist. Please create it first.")
    
    def activate_environment(self):
        if self.environment_exists():
            # Instructions to activate the environment (platform-specific)
            if sys.platform == "win32":
                activation_command = f"{self.environment_name}\\Scripts\\activate"
            else:
                activation_command = f"source {self.environment_name}/bin/activate"
            print(f"To activate the virtual environment, run:\n{activation_command}")
        else:
            print(f"Virtual environment '{self.environment_name}' does not exist. Please create it first.")
    
    def read_log_file(self, log_file_path):
        # Read and process log file
        try:
            with open(log_file_path, 'r') as file:
                data = file.readlines()
                # Process the log data as needed
                print(f"Log data from '{log_file_path}' read successfully.")
                return data
        except Exception as e:
            print(f"Failed to read log file '{log_file_path}': {e}")
            return None
    
    def import_csv_file(self, csv_file_path):
        # Read and process CSV file
        try:
            data = pd.read_csv(csv_file_path)
            print(f"CSV data from '{csv_file_path}' imported successfully.")
            return data
        except Exception as e:
            print(f"Failed to import CSV file '{csv_file_path}': {e}")
            return None
    
    def setup(self):
        self.create_environment()
        self.install_libraries()
        self.activate_environment()

# Usage
if __name__ == "__main__":
    setup = EnvironmentSetup()
    setup.setup()
    
    # Example usage of new methods
    log_data = setup.read_log_file('path/to/log/file.log')
    if log_data is not None:
        print(log_data[:5])  # Print first 5 lines of log data

    csv_data = setup.import_csv_file('path/to/run_data.csv')
    if csv_data is not None:
        print(csv_data.head())  # Print first 
