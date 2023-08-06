# Owon SPEx103 PSU python control library
This library works with the Owon SPE6103 and SPE3103 power supplies.

## Example Usage with context manager
```python
from owon_psu import OwonPSU

with OwonPSU("/dev/ttyUSB0") as opsu:
  print("Identity:", opsu.read_identity())
  print("Voltage:", opsu.measure_voltage())
  print("Current:", opsu.measure_current())

  opsu.set_voltage(20)
  opsu.set_current(2)
  opsu.set_voltage_limit(30)
  opsu.set_current_limit(3)
  print("Output enabled:", opsu.get_output())
  opsu.set_output(True)
```

## Example Usage without context manager
```python
from owon_psu import OwonPSU

opsu = OwonPSU("/dev/ttyUSB0")
print("Identity:", opsu.read_identity())
print("Voltage:", opsu.measure_voltage())
print("Current:", opsu.measure_current())
opsu.set_voltage(20)
opsu.set_current(2)
opsu.set_voltage_limit(30)
opsu.set_current_limit(3)
print("Output enabled:", opsu.get_output())
opsu.set_output(True)
```