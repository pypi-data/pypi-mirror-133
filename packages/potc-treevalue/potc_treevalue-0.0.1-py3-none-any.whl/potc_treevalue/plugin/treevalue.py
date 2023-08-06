from potc.fixture import rule, Addons
from treevalue import raw, TreeValue
from treevalue.tree.common import RawWrapper, TreeStorage, create_storage


@rule(type_=RawWrapper)
def treevalue_raw(v: RawWrapper, addon: Addons):
    return addon.obj(raw)(v.value())


@rule(type_=TreeStorage)
def treevalue_storage(v: TreeStorage, addon: Addons):
    return addon.obj(create_storage)(v.dump())


@rule(type_=TreeValue)
def treevalue_tree(v: TreeValue, addon: Addons):
    return addon.obj(type(v))(v._detach().dump())
