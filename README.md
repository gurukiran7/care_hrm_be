# Care HRM

Care HRM is a plugin for CARE that adds comprehensive human resource management features, including employee profiles, leave and holiday tracking, and secure document handling.

## Features

- Employee profile management with creation, update, and retrieval
- Leave request application, approval, and tracking
- Automated leave balance calculation
- Holiday management and calendar integration
- Secure employee document upload and archiving
- Advanced filtering and search for HR data
- Role-based authorization for all HR actions

## Installation

To install care HRM, you can add the plugin config in [care/plug_config.py](https://github.com/ohcnetwork/care/blob/develop/plug_config.py) as follows:


```python
...

plugs = [
    Plug(
        name="hrm",
        package_name="plugins/care_plugin_hrm",
        version="",
        configs={},
    ),
]

...
```
