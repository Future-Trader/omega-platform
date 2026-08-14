class OCGFError(Exception):
    """Base OCGF exception."""


class GeneratorError(OCGFError):
    """Generator execution failure."""


class TemplateError(OCGFError):
    """Template rendering failure."""


class FileGenerationError(OCGFError):
    """File creation or modification failure."""


class ValidationError(OCGFError):
    """Generated project validation failure."""


class RegistryError(OCGFError):
    """Generator registry failure."""


class ManifestError(OCGFError):
    """Manifest operation failure."""


class ConfigurationError(OCGFError):
    """Configuration failure."""