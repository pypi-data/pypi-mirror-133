

class ConfigTemplaterError(Exception):
    pass


class ConfigTemplaterPackageError(ConfigTemplaterError):
    pass


class ConfigTemplaterFileNotFoundError(ConfigTemplaterError):
    pass
