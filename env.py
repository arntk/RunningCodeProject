import subprocess
import sys

class EnvironmentSetup:
    def __init__(self, environment_name='env'):
        self.environment_name = environment_name
    
    def create_environment(self):
        # Create virtual environment
        subprocess.check_call([sys.executable, '-m', 'venv', self.environment_name])
        print(f"Virtual environment '{self.environment_name}' created.")
    
    def install_libraries(self):
        # List of necessary libraries
        libraries = ['openai', 'pandas', 'matplotlib', 'numpy', 'scikit-learn']
        
        # Install each library using pip
        for lib in libraries:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
            print(f"Library '{lib}' installed.")
    
    def activate_environment(self):
        # Instructions to activate the environment (platform-specific)
        if sys.platform == "win32":
            activation_command = f"{self.environment_name}\\Scripts\\activate"
        else:
            activation_command = f"source {self.environment_name}/bin/activate"
        print(f"To activate the virtual environment, run:\n{activation_command}")
    
    def setup(self):
        self.create_environment()
        self.install_libraries()
        self.activate_environment()

# Usage
if __name__ == "__main__":
    setup = EnvironmentSetup()
    setup.setup()