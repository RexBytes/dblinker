import yaml
from pathlib import Path
from copy import deepcopy
from importlib import resources


class SettingsManager:
    def __init__(self, settings_filename='app_settings.yaml'):
        # Path to the default settings file
        self.settings_file = Path(__file__).resolve().parent / settings_filename
        # Load settings from the default settings file
        self.settings = self.load_initial_settings()
        # Use the package name from the settings
        self.package_name = self.settings.get('appPackageName')
        # Set up user configuration environment (directories, template file)
        self.setup_user_config()  # Ensure directories and template file are set up
        # Load user-specific settings, if they exist
        self.user_settings = self.load_user_settings()
        # Merge settings
        self.merge_settings()

    def load_initial_settings(self):
        """Load initial settings from app_settings.yaml located in the same directory as this class."""
        if not self.settings_file.exists():
            raise FileNotFoundError(f"Could not find the settings file {self.settings_file}")
        with open(self.settings_file, "r") as file:
            return yaml.safe_load(file)

    def load_user_settings(self):
        """Load user override settings if available."""
        # Construct the path to the user settings file based on information from the default settings
        user_config_dir = self.settings.get('appStubConfigDir')
        user_config_filename = self.settings.get('appStubConfigFile')
        user_config_path = Path.home() / user_config_dir / user_config_filename

        if user_config_path.exists():
            with open(user_config_path, "r") as file:
                user_settings = yaml.safe_load(file)
                if user_settings is not None:  # Check if user_settings is not None
                    print("User settings loaded successfully:", user_settings)
                    return user_settings
                else:
                    print("User settings file is empty or invalid:", user_config_path)
        else:
            print("User settings file not found:", user_config_path)
        return {}

    def save_user_settings(self, new_settings):
        """Save user settings to the user config file and update in-memory settings."""
        # First, merge the new settings with any existing user settings
        self.user_settings.update(new_settings)

        # Then, write the user settings to the user config file
        user_config_dir = self.settings.get('appStubConfigDir')
        user_config_filename = self.settings.get('appStubConfigFile')
        user_config_path = Path.home() / user_config_dir / user_config_filename

        # Ensure the directory exists
        user_config_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the user settings to the file
        with open(user_config_path, 'w') as file:
            yaml.dump(self.user_settings, file, default_flow_style=False)

        # Merge the user settings into the current settings to update the class state
        self.merge_settings()

    def merge_settings(self):
        """Override package settings with any user settings."""
        package_settings = self.load_initial_settings()  # Reload the default package settings
        self.settings = deepcopy(package_settings)  # Start with a deep copy of the package settings
        if self.user_settings:
            # Update with any user settings that are not None
            self.settings.update({k: v for k, v in self.user_settings.items() if v is not None})

    def ensure_directory_exists(self, dir_path):
        """Ensure the specified directory exists."""
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    def ensure_absolute_path(self, path_list):
        """Ensure the constructed path is absolute if the path list begins with an empty string."""
        if path_list and path_list[0] == '':
            # Prepend the root directory to the path list if not already absolute
            return Path('/', *path_list)
        else:
            # Construct a path normally if the first element is not an empty string
            return Path(*path_list)

    def setup_user_config(self):
        """Set up user config file and ensure connection config directory exists."""
        # Create the base stub config directory
        # Example of adjusting the path construction
        stub_config_dir = self.ensure_absolute_path(self.settings.get('appStubConfigDir', []))
        self.ensure_directory_exists(stub_config_dir)

        # Path to the user settings file within the stub config directory
        user_config_filename = self.settings.get('appStubConfigFile')  # Simplified to just the filename
        user_config_path = stub_config_dir / user_config_filename

        # Copy the user config template if the user config file does not exist
        if not user_config_path.exists():
            package_name = self.settings.get('appPackageName')
            subpath_within_package = 'common.templates'  # Subpath within the package
            full_package_path = f'{package_name}.{subpath_within_package}'
            try:
                # Using the resources.open_binary function to open the file for reading
                with resources.open_binary(full_package_path, user_config_filename) as template_file:
                    content = template_file.read()
                # Now write this content to the user_config_path
                with open(user_config_path, 'wb') as user_file:
                    user_file.write(content)
            except FileNotFoundError:
                print(
                    f"Warning: Template file '{user_config_filename}' not found in the package '{full_package_path}'.")

        # The connection config directory should also be ensured to exist
        connection_config_dir = Path.home() / Path(*self.settings.get('appConnectionConfigDir'))
        self.ensure_directory_exists(connection_config_dir)

    # Add any additional methods you need for your SettingsManager below...
