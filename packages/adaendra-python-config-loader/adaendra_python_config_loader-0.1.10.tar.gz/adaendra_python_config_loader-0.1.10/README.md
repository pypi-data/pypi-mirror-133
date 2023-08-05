# Python Config Loader

![badge](https://img.shields.io/badge/version-0.1.0-blue)

The objective of this library is to easily load external configs for a Python project and use it for anywhere 
in your project.

---

## How to use it
Install with pip
> pip install adaendra-python-config-loader

Import the configs and use it!
```python
from AdaendraConfigs import AdaendraConfigs

print(AdaendraConfigs.configs.abc)
```

## Environment variables
|Name|Description|Default value|
|---|---|---|
|CONFIG_ENVIRONMENT|Environment to load|*None*|
|CONFIG_FOLDER|Path to the config files|'/app/resources'|
|CONFIG_FILE_EXTENSION|File extensions of your config file. Allow : '.yml'/'.yaml'/'.json'|'.yaml'|
|CONFIG_PROJECT_NAME|Name of your project *(which is generally the name of the config files)*|'application'|

---

## Documentation
- [PyPi](./documentation/pypi.md)
