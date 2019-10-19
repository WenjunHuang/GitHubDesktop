import pinject

from desktop.binding_specs import AppBindingSpec
from desktop.object_graph import set_object_graph
from desktop.register_qml_types import register_qml_types


class ConfigPathBindingSpec(pinject.BindingSpec):
    def __init__(self, config_dir: str):
        self.config_dir = config_dir

    def provide_config_dir(self):
        return self.config_dir


def run_app(bootstrap_class, config_dir: str):
    obj_graph = pinject.new_object_graph(binding_specs=[ConfigPathBindingSpec(config_dir), AppBindingSpec()])
    set_object_graph(obj_graph)
    register_qml_types()

    bootstrap = obj_graph.provide(bootstrap_class)
    bootstrap.run()
