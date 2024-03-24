from importlib import resources
import yaml


def load_app_settings():
    """Load application-wide settings from the YAML file using importlib.resources."""
    # Use importlib.resources to access the app_settings.yaml file packaged with the distribution
    with resources.files("dblinker").joinpath("app_settings.yaml") as path:
        # The as_file context manager is used for compatibility with resources that may not have a direct filesystem
        # path
        with resources.as_file(path) as config_file:
            # Open the app_settings.yaml file and load its contents
            with open(config_file, "r") as file:
                settings = yaml.safe_load(file)
    return settings


# Example usage
if __name__ == "__main__":
    appsettings = load_app_settings()
    print(appsettings)
