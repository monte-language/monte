from monte.runtime.guards.base import PythonTypeGuard
from monte.runtime.tables import ConstList, MonteMap

listGuard = PythonTypeGuard(ConstList, "list")
mapGuard = PythonTypeGuard(MonteMap, "map")
