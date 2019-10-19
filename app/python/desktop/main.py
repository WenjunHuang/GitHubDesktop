import pinject

from desktop.bootstrap import Bootstrap
from desktop.lib.binding_specs import AppBindingSpec
from desktop.register_qml_types import register_qml_types


obj_graph = pinject.new_object_graph(binding_specs=[AppBindingSpec()])
register_qml_types()
bootstrap = obj_graph.provide(Bootstrap)
bootstrap.run()
