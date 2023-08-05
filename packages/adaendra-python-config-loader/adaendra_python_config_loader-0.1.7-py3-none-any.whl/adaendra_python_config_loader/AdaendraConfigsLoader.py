import os
import yaml
from adaendra_python_config_loader.Constants import ENV_CONFIG_FOLDER, ENV_CONFIG_PROJECT_NAME, \
    ENV_CONFIG_FILE_EXTENSION, ENV_CONFIG_ENVIRONMENT, \
    DEFAULT_CONFIG_FOLDER, DEFAULT_CONFIG_PROJECT_NAME, DEFAULT_CONFIG_FILE_EXTENSION, \
    FILE_EXT_YAML, FILE_EXT_YML, FILE_EXT_JSON


def get_config_folder() -> str:
    """
    Retrieve the config folder.
    If the environment variable DEFAULT_CONFIG_FOLDER is fill, take its value.
    Otherwise, take the default value.
    :return: str - The config folder.
    """
    config_folder = DEFAULT_CONFIG_FOLDER
    if os.getenv(ENV_CONFIG_FOLDER) is not None:
        config_folder = os.getenv(ENV_CONFIG_FOLDER)
    return config_folder


def get_config_project_name() -> str:
    """
    Retrieve the config project name.
    If the environment variable DEFAULT_CONFIG_PROJECT_NAME is fill, take its value.
    Otherwise, take the default value.
    :return: str - The config project name.
    """
    config_project_name = DEFAULT_CONFIG_PROJECT_NAME
    if os.getenv(ENV_CONFIG_PROJECT_NAME) is not None:
        config_project_name = os.getenv(ENV_CONFIG_PROJECT_NAME)
    return config_project_name


def get_config_file_extension() -> str:
    """
    Retrieve the config file extension.
    If the environment variable DEFAULT_CONFIG_FILE_EXTENSION is fill, take its value.
    Otherwise, take the default value.
    :return: str - The config file extension.
    """
    config_file_extension = DEFAULT_CONFIG_FILE_EXTENSION
    env_config_file_extension = os.getenv(ENV_CONFIG_FILE_EXTENSION)
    if env_config_file_extension is not None and (env_config_file_extension == FILE_EXT_YAML
                                                  or env_config_file_extension == FILE_EXT_YML
                                                  or env_config_file_extension == FILE_EXT_JSON):
        config_file_extension = os.getenv(ENV_CONFIG_FILE_EXTENSION)
    return config_file_extension


def get_config_environment() -> str:
    """
    Retrieve the config environment.
    If the environment variable ENV_CONFIG_ENVIRONMENT is fill, take its value.
    Otherwise, no environment will be defined.
    :return: str - The config environment.
    """
    config_environment = None
    if os.getenv(ENV_CONFIG_ENVIRONMENT) is not None:
        config_environment = os.getenv(ENV_CONFIG_ENVIRONMENT)
    return config_environment


def get_file_list() -> list:
    """
    Build the list of configs files to load.
    :return: list[str]
    """
    # The common config file
    file_list = [get_config_folder() + "/" + get_config_project_name() + get_config_file_extension()]

    # The environment config file
    if get_config_environment() is not None:
        file_list.append(get_config_folder() + "/" + get_config_project_name() + "-" + get_config_environment() + get_config_file_extension())

    return file_list


def load_configs():
    """
    Retrieve the configs from the configs files and load it into the config singleton.
    """
    config_dict = {}
    for file_path in get_file_list():
        try:
            with open(file_path) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                tmp_config_dict = yaml.load(file, Loader=yaml.FullLoader)

                config_dict = config_dict | tmp_config_dict
        except FileNotFoundError:
            print('[AdaendraConfigsLoader] - File not found : ' + file_path)

    return config_dict


#if __name__ == "__main__":
#    load_configs()
