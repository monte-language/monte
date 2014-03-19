from monte.runtime.guards.base import PythonTypeGuard
from monte.runtime.tables import ConstList, ConstMap

listGuard = PythonTypeGuard(ConstList, "list")
mapGuard = PythonTypeGuard(ConstMap, "map")
