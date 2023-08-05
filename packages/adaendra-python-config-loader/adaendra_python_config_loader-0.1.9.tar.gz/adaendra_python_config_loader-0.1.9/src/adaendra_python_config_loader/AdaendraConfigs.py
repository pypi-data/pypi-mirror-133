from adaendra_immutable_dict.AdaendraImmutableDict import AdaendraImmutableDict


class AdaendraConfigs(object):
    """
    The config loader.
    """

    # --- PARAMETERS
    configs = None

    # --- METHODS
    def __new__(cls, config_dict: dict):
        if not AdaendraConfigs.configs:
            AdaendraConfigs.configs = AdaendraConfigs.__AdaendraConfigs(config_dict)
        return AdaendraConfigs.configs

    def __getattr__(self, name):
        if not AdaendraConfigs.configs:
            raise AttributeError(
                f"No configs were loaded on start."
            )
        return getattr(self.configs, name)

    def __getattribute__(self, name):
        if not AdaendraConfigs.configs:
            raise AttributeError(
                f"No configs were loaded on start."
            )
        return getattr(self.configs, name)

    def __setattr__(self, name):
        """
        Unsupported method, will raise a TypeError.
        :raise: TypeError
        """
        raise TypeError(
            f"The configs can't be changed."
        )

    # --- INTERNAL CLASSES
    class __AdaendraConfigs:
        """
        The internal class to generate the singleton.
        """

        # --- METHODS
        def __init__(self, configs_dict: dict):
            self.configs_dict = AdaendraImmutableDict(configs_dict)

        def __str__(self):
            return "Configs : " + self.configs_dict.__repr__()

        def __getattr__(self, name):
            return self.configs_dict[name]


__all__ = (AdaendraConfigs.__name__,)
