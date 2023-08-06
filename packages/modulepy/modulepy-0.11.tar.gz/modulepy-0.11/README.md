# modulepy

easily build modular applications

## installation

```shell
pip3 install modulepy
# or
pip3 install git+https://github.com/nbdy/modulepy
```

## features

- [X] module baseline
  - [X] thread based module
  - [X] process based module
- [X] module loader
  - [X] one-line module loading
  - [X] one-line directory loading
- [X] module manager
  - [X] add module
  - [X] remove module
  - [X] reload module directory
  - [X] module dependency resolution
  - [X] ipc

## usage

```python
from modulepy import ModuleInformation, ModuleVersion, SharedData, ModuleBase
from modulepy.manager import ModuleManager
from time import sleep


class ModuleA(ModuleBase):
    information = ModuleInformation("A", ModuleVersion(1, 0, 0))
    dependencies = [ModuleInformation("B", ModuleVersion(1, 0, 0))]

    def work(self):
        self.enqueue({"A": 0})

    def process_input_data(self, data: SharedData):
        print(data)


class ModuleB(ModuleBase):
    information = ModuleInformation("B", ModuleVersion(1, 0, 0))

    def work(self):
        self.enqueue({"B": 1})


def dependency_missing(module):
    print(f"Dependency for module {module.name} missing: {module.dependencies}")


if __name__ == '__main__':
    manager = ModuleManager()
    manager.on_dependency_missing = dependency_missing
    manager.add_module(ModuleB())
    manager.add_module(ModuleA())
    manager.start()
    sleep(3)
    manager.stop()

```