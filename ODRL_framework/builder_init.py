# ordl_framework/builders_init.py
from .core.registry import builder_registry
from .models.radio import Radio
from .models.modulation import Modulation
from .models.interface import Interface

@builder_registry.register("radio")
def build_radio(data):
    mods = [Modulation(m["type"], m["parameters"]) for m in data["modulations"]]
    intfs = Interface(data["interfaces"]["rx"], data["interfaces"]["tx"])
    return Radio(
        name=data["name"],
        frequency_range=data["frequency_range"],
        bandwidth=data["bandwidth"],
        modulations=mods,
        interfaces=intfs
    )

@builder_registry.register("Storage")
def build_storage(data):
    return Storage(**data)


class Storage:
    def __init__(self, id, capacity_gb, used_gb, **kwargs):
        self.id = id
        self.capacity_gb = capacity_gb
        self.used_gb = used_gb

    def __repr__(self):
        return f"<Storage {self.id}: {self.used_gb}/{self.capacity_gb} GB>"


        self.used_gb = used_gb

    def __repr__(self):
        return f"<Storage {self.id}: {self.used_gb}/{self.capacity_gb} GB>"


