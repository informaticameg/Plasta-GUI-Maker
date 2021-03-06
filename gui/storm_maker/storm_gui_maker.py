#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Jonathan Ferreyra <jalejandroferreyra@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os,sys
from PyQt4 import QtCore, QtGui, uic
from gui.mytablewidget import MyTableWidget
from maker import add_maker_simple as gui_maker
from maker.logic_storm_class import LogicStormClass


#TODO: autosugerir el nombre de la clase al nombre del archivo para guardar
#TODO: permitir crear paquete __init__ del objeto en cuestion

class StormGuiMaker(QtGui.QMainWindow):

    def __init__(self, parent = None):
        FILENAME = 'storm_gui_maker.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        #self.setWindowState(QtCore.Qt.WindowMaximized)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
        self.padre = parent

        self.tablaAtributos = MyTableWidget(
            self.twLista,
            ["Atributo","Storm Type","Widget","Valor por defecto",
            "Primario","Not Null","Referencia","Cruzada"]
        )

        self.widgets = {}
        self.atributos = []

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self):
        valido = True
        if self.leNombre.text().isEmpty() :
            self.leNombre.setStyleSheet('background-color: rgb(255, 155, 155);')
            valido = False

        if self.leNombreClase.text().isEmpty() :
            self.leNombreClase.setStyleSheet('background-color: rgb(255, 155, 155);')
            valido = False

        if valido == True :
            self.agregarALista()
            self.leNombre.setFocus()

    @QtCore.pyqtSlot()
    def on_btQuitar_clicked(self):
        # obtiene el indice en la lista en donde esta ubicado el elemento seleccionado
        indice = self.tablaAtributos.getSelectedCurrentIndex()
        del self.atributos[ indice ]
        # vuelve a cargar la lista
        items = [
        [dic['atributo'],dic['storm_type'],dic['widget'],dic['default'],
        dic['primario'],dic['not_null'],dic['referencia'],dic['cruzada'] ]
            for dic in self.atributos.values()]

        self.tablaAtributos.addItems( items )

    @QtCore.pyqtSlot()
    def on_btExaminar_clicked(self):
        self.leUbicacion.setText(
            self.guardarArchivoPython())

    @QtCore.pyqtSlot()
    def on_btGenerar_clicked(self):
        if not self.leUbicacion.text().isEmpty() :
            self.generar()
        else:
            self.leUbicacion.setStyleSheet('background-color: rgb(255, 155, 155);')

    def on_twLista_doubleClicked(self , index):
        pass

    def on_clbtLevantarClaseStorm_pressed(self):

        print self.load_from_file( self.abrirArchivoPython() )

    @QtCore.pyqtSlot()
    def on_gbReferencia_clicked(self):
       self.leNombreReferencia.setText(
           unicode(self.leNombre.text().toUtf8(),'utf-8').capitalize())

    def on_twLista_doubleClicked(self , index):
        datos = self.tablaAtributos.getRowString()

########################################################################

    def guardarArchivoPython(self):
        u""" Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        nombre_archivo = unicode(self.leNombreClase.text().toUtf8(),'utf-8')
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        filename = dialog.getSaveFileName(self, 'Abrir archivo Python',filter='*.py')
        if filename != '' :
            filename = unicode(filename, 'utf-8') + '.py'

            return filename
        else:
            return ''

    def abrirArchivoPython(self):
        u""" Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        nombre_archivo = unicode(self.leNombreClase.text().toUtf8(),'utf-8')
        dialog = QtGui.QFileDialog()
        filename = dialog.getOpenFileName(self, 'Abrir archivo Python',filter='*.py')
        if filename != '' :
            filename = unicode(filename, 'utf-8') + '.py'

            return filename
        else:
            return ''

    def generar(self):
        logSC = LogicStormClass()

        destino = unicode(self.leUbicacion.text().toUtf8(),'utf-8')
        nombre_clase = unicode(self.leNombreClase.text().toUtf8(),'utf-8')

        if self.chkGenerarClase.isChecked() :
            logSC.generarClase(
                destino,
                nombre_clase,
                self.convertirListaAtributosADiccionarioAtributos( self.atributos ),
                package = self.chkGenerarPaquete.isChecked())

        if self.chkGenerarUi.isChecked() :
            destino = destino[:-3] + '.ui'
            gui_maker.generarUI(
                destino,
                self.widgets,
                opciones = {'tipo':'Dialog'},
                botones = {'bt_salir_guardar':True})
        QtGui.QMessageBox.information(self, "Generar clase Storm + .ui",u"Generación realizada con éxito")

    def agregarALista(self):
        elemento = self.getTextWidgets(
            self.leNombre,
            self.cbStormType,
            self.cbWidget,
            self.leValorPorDefecto)
        elemento += ['True'] if self.btPrimario.isChecked() else ['False']
        elemento += ['True'] if self.btNotNull.isChecked() else ['False']

        if self.gbReferencia.isChecked() :
            referencia = self.getTextWidgets(
            self.leNombreReferencia,
            self.chkCruzada)
            elemento += referencia
        else:
            elemento += ['','']

        self.atributos.append( elemento )
        # agrega una fila a la tabla
        self.tablaAtributos.appendItem( elemento )

        self.reestablecerCampos()

        # atributo - widget - referencia
        self.agregarWidget(elemento[0], elemento[2], elemento[6])

    def agregarWidget(self, atributo, widget_tipo, referencia):
        self.widgets[ len(self.widgets) ] = {
        'atribute':atributo,
        'widget_type':widget_tipo,
        'reference':referencia
        }

    def convertirListaAtributosADiccionarioAtributos(self, atributos):
        resultado = {}
        for atributo in atributos:
            un_atributo = self.convertToDict(
                ["atributo","storm_type","widget","default","primario","not_null","referencia","cruzada"],
                atributo
            )
            # agrega un atributo para generarse
            resultado[ len(resultado) ] = un_atributo
        return resultado

    def cargarWidgets(self,datos, widgets):
        import PyQt4

        for dato, widget in zip(datos,widgets):
            if type(widget) is PyQt4.QtGui.QLineEdit :
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QComboBox:
                widget.setCurrentIndex(
                    widget.findText(dato))
            elif type(widget) is PyQt4.QtGui.QLabel:
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QTextEdit:
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QDateEdit:
                if len(dato) == 4 :
                    widget.setDate(PyQt4.QtCore.QDate(int(dato),1,1))
                elif len(dato) == 10 :
                    widget.setDate(PyQt4.QtCore.QDate(
                        int(dato[6:]),int(dato[3:5]),int(dato[:2])))
            elif type(widget) is PyQt4.QtGui.QSpinBox:
                widget.setValue(int(dato))
            elif type(widget) is PyQt4.QtGui.QCheckBox:
                if dato == 'True' :
                    widget.setChecked(True)
                else:
                    widget.setChecked(False)

    def getTextWidgets(self, * widgets):
        """
        Devuelve una lista con el valor cargado segun el widget
        """
        import PyQt4
        values = []
        for widget in widgets :
            if type(widget) is PyQt4.QtGui.QLineEdit :
                values.append(
                    unicode(widget.text().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QComboBox:
                values.append(
                    unicode(
                        widget.itemText(widget.currentIndex()).toUtf8(),
                        'utf-8'))
            elif type(widget) is PyQt4.QtGui.QLabel:
                values.append(
                    unicode(widget.text().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QDateEdit:
                values.append(
                    unicode(
                        widget.date().toString(widget.displayFormat()).toUtf8(),
                        'utf-8'))
            elif type(widget) is PyQt4.QtGui.QTextEdit:
                values.append(
                    unicode(widget.toPlainText().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QSpinBox:
                values.append(
                    unicode(str(widget.value()),'utf-8')
                    )
            elif type(widget) is PyQt4.QtGui.QCheckBox :
                if widget.isChecked() == True :
                    values.append('True')
                else:
                    values.append('False')

        return values

    def convertToDict(self, columnas, datos):
        resultado = {}
        for columna, valor in zip(columnas, datos) :
            resultado[columna] = valor
        return resultado

    def reestablecerCampos(self):
        self.cargarWidgets(
             [
             "",
             "Unicode",
             "QLineEdit",
             "",
             "",
             "False"
            ],
            [
             self.leNombre,
             self.cbStormType,
             self.cbWidget,
             self.leValorPorDefecto,
             self.leNombreReferencia,
             self.chkCruzada
             ]
        )
        self.btPrimario.setChecked(False)
        self.btNotNull.setChecked(False)
        self.gbReferencia.setChecked(False)

    def obtenerClaseDesdeArchivo(self, module_name, class_name):
#        globals()['QsciLexer'+lenguaje]()#cargador magico de clases
        try:
          __import__(module_name)
          modul = sys.modules[module_name]
          instance = modul.class_name() # obviously this doesn't works, here is my main problem!
          print instance
        except ImportError, msg:
           # manage import error
           print msg

    def load_from_file(self, filepath):
        import imp
        class_inst = None
        expected_class = 'MyClass'

        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
        py_mod = None
        print 'mod_name, filepath>',mod_name, filepath[:-3]
        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name[:-3], filepath[:-3])
            print py_mod

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)

        if expected_class in dir(py_mod):
            print 'expected_class>',expected_class
            class_inst = py_mod.MyClass()

        return class_inst

def main():
    app = QtGui.QApplication(sys.argv)
    window = StormGuiMaker()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
