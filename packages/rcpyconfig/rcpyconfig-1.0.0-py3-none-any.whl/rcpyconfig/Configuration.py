from typing import TypeVar, Type, Callable

from rcpyutils import DictUtils
import yaml


T = TypeVar('T', bound=yaml.YAMLObject)

PREFIX_PATH_SEPARATOR = '.'


# Configuration class decorator
def configuration_properties(_cls: Type[T] | None = None, *, prefix: str = "application") -> Callable[
    [Type[T]], Type[T]]:
    def prepare_yaml_property(cls: Type[T]) -> Type[T]:
        cls.yaml_loader = yaml.SafeLoader
        cls.yaml_tag = f"!{prefix}"

        def constructor(safe_loader, node):
            fields = safe_loader.construct_mapping(node)
            return cls(**fields)

        loader = yaml.SafeLoader
        yaml.add_constructor(cls.yaml_tag, constructor, Loader=loader)
        yaml.add_path_resolver(cls.yaml_tag, prefix.split(PREFIX_PATH_SEPARATOR), dict, Loader=loader)
        return cls

    return prepare_yaml_property(_cls) if _cls else prepare_yaml_property


# Load rcpyconfig function
def load_yaml_configuration(config_file_path: str, configuration_class: Type[T]) -> T:
    with open(config_file_path, 'r') as config_file:
        return DictUtils.get_value_from_path(
            dictionary=yaml.safe_load(config_file),
            path=configuration_class.yaml_tag[1:].split(PREFIX_PATH_SEPARATOR),
            default_supplier=lambda: configuration_class()
        )
