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
from modulepy import ThreadModule, ProcessModule, ModuleInformation, ModuleVersion, SharedData
from modulepy.manager import ModuleManager


class ModuleA(ThreadModule):
    information = ModuleInformation("A", ModuleVersion(1, 0, 0))
    dependencies = [ModuleInformation("B", ModuleVersion(1, 0, 0))]

    def work(self):
        self.data_enqueue({"A": 0})

    def process_input_data(self, data: SharedData):
        print(data)


class ModuleB(ProcessModule):
    information = ModuleInformation("B", ModuleVersion(1, 0, 0))

    def work(self):
        self.data_enqueue({"B": 1})


if __name__ == '__main__':
    manager = ModuleManager()
    manager.add_module(ModuleA())
    manager.add_module(ModuleB())
    manager.start()
    manager.join()

```