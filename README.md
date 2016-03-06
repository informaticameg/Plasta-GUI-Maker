# Plasta GUI Maker

> Set of utilities and tools for working with [Plasta](https://github.com/informaticameg/plasta) and interfaces in PyQt.

## List of utilities/tools

All these tools described below have a GUI to do the same as from code.

### Generate Plasta package

Tool for generate the 4 files of Plasta base package.

```
/object_folder_example
  --- __init__.py
  --- manager.py
  --- add.py
  --- gui.py
```
From code:

```python
from maker import make_plasta_package
data = {
  'className':'Person',
  'addIdeAttr':True,
  'attributes':[
      {'name':'name','type':'Unicode'},
      {'name':'last_name','type':'Unicode'},
      {'name':'email','type':'Unicode'},
      {'name':'age','type':'Int'},
      {'name':'birthday','type':'Date'},
    ],
  'widgetToAttr':{
    'name':'lineEdit',
    'last_name':'lineEdit',
    'email':'lineEdit',
    'age':'spinBox',
    'birthday':'dateEdit',
  },
  'classesToGenerate':{
    'storm':True,'manager':True,'gui':True,'add':True
  },
  'outputFolder':'/some_folder'
}

make_plasta_package.generatePackage(data)
```

### Create UI

Tool for generate .ui file like a form new/edit

```python
from maker import add_maker_simple

outputFolder = '/some_output_folder/some_file.ui'
fields = {0: {u'field1': u'QLineEdit'}, 1: {u'field2': u'QLineEdit'}}
buttons = {'bt_limpiar': False, 'bt_cancelar_aceptar': False, 'bt_salir_guardar': True, 'bt_salir_aceptar': False}
options = {'tipo': 'Dialog', 'generar_plantilla': False}

add_maker_simple.generarUI(outputFile, fields, buttons, options)
```

#### Values for 'options' parameter:
- tipo: type of window to generate, possible values: (Dialog, MainWindow)
- generar_plantilla: if True, will be generate together with the .ui the .py file to handle

### Generate Storm class + .ui

Template generator for the storm file `__init__.py`. Data types are supported for databases SQLite, MySQL y PostgresSQL.

### Generate signals/events

Generator/explorer of signals/events of the widgets included in a .ui

### Generate template for .ui file

Generate the .py file for a .ui file


## TODO
* **Create UI**
	* Include signals/events methods
* **Generate signals/events**
	* Functionality buttons located to the left of code editors
* **Generate Storm class + .ui** 
	* Generate the .ui file for the  template

## Run the program
```python 
python main.py
```

## Test

```python 
python run_test.py
```

## Contribute

Contributions are welcome :)
