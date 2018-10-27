'''
Created on 5. 11. 2017

@author: Lukas Bilek

This is an application for Boulder Media - test


'''

import os
import sys
import atexit
import json
from zipfile import ZipFile
from shutil import copytree
import shutil

try:
    from PySide import QtGui, QtCore, QtUiTools, QtCore
    from PySide.QtCore import QVariant
    from PySide import Qt as qt
    run_modules = 'PySide'

except:
    from PyQt4 import QtGui, QtCore, uic, QtCore
    from PyQt4.QtCore import QVariant
    from PyQt4 import Qt as qt
    run_modules = 'PyQt'

path = os.path.realpath(__file__)
dir_path = os.path.dirname(path)
print dir_path



class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        # prepare window
        super(MyWidget, self).__init__(parent)
        
        # load window ui
        self.myWidget = self.load_ui("work_area_gui.ui")
        
        # connect window buttons with functions
        '''self.myWidget.textEdit.textChanged.connect(self.text)
        self.myWidget.actionFont.triggered.connect(self.font)
        self.myWidget.actionColour.triggered.connect(self.color)'''
        
        self.myWidget.pushButton_loadWorkArea.pressed.connect(self.loadWorkAreaDir)
        self.myWidget.pushButton_storeWorkArea.pressed.connect(self.storeWorkAreaDir)
        self.myWidget.pushButton_saveWorkArea.pressed.connect(self.saveWorkArea)
        self.myWidget.listWidget_versions.itemClicked.connect(self.readDescription)
        self.myWidget.pushButton_restoreWorkArea.pressed.connect(self.restoreWorkArea)
        
        # temporarily 
        #self.myWidget.lineEdit_loadWorkArea.setText('/home/moner/workspace/python_tests/boulder_media/test_folders/load_folder/directory')
        #self.myWidget.lineEdit_storeWorkArea.setText('/home/moner/workspace/python_tests/boulder_media/test_folders/save_folder')

        self.checkArchives()
        self.treeDir()
        
        self.myWidget.statusbar.showMessage('Ready')
        
        self.myWidget.show()

    def restoreWorkArea(self):
        
        get_item = str(self.myWidget.listWidget_versions.selectedItems()[0].text())
        save_work_dir = str(self.myWidget.lineEdit_storeWorkArea.text().replace('\\','/'))        
        load_work_dir = str(self.myWidget.lineEdit_loadWorkArea.text().replace('\\','/'))
        try:shutil.rmtree(os.path.dirname(load_work_dir) +'/'+ os.path.basename(load_work_dir) + '/')
        except:
            pass
        copytree(save_work_dir + '/' + get_item + '/' + os.listdir(save_work_dir + '/' + get_item )[0], os.path.dirname(load_work_dir) +'/'+ os.path.basename(load_work_dir))
        
        self.treeDir()
        
        self.myWidget.statusbar.showMessage('The work area has been restored from version: {}'.format(get_item))
    
    def readDescription(self):
        get_item = str(self.myWidget.listWidget_versions.selectedItems()[0].text())
        save_work_dir = str(self.myWidget.lineEdit_storeWorkArea.text().replace('\\','/'))
        with open(save_work_dir + "/"+get_item+'.json') as json_data:
            d = json.load(json_data)
            self.myWidget.textEdit_DescriptionFromVersion.setPlainText(d['description'])
            
        self.myWidget.statusbar.showMessage('The description has been loaded: {}'.format(get_item))
    def checkArchives(self):
        
        load_work_dir = str(self.myWidget.lineEdit_loadWorkArea.text().replace('\\','/'))
        save_work_dir = str(self.myWidget.lineEdit_storeWorkArea.text().replace('\\','/'))
        load_folder = load_work_dir.split('/')[-1]
        save_folder = save_work_dir.split('/')[-1]
        
        list_dir = os.listdir(save_work_dir)
        print list_dir
        list_json = [x for x in list_dir if '.json' in x]        
        
        [self.myWidget.listWidget_versions.addItem(i[:-5]) for i in sorted(list_json)]

    def saveWorkArea(self):
        '''
        Save work area in the right directory and check out versions
        Also save description as save work as zip with readme.md
        '''
        load_work_dir = str(self.myWidget.lineEdit_loadWorkArea.text().replace('\\','/'))
        save_work_dir = str(self.myWidget.lineEdit_storeWorkArea.text().replace('\\','/'))
        load_folder = load_work_dir.split('/')[-1]
        save_folder = save_work_dir.split('/')[-1]
        
        list_dir = os.listdir(save_work_dir)
        print list_dir
        list_folders = [x for x in list_dir if '.' not in x]

        file = open(save_work_dir+'/readme.md','w') 
         
        file.write('hello there') 
         
        file.close() 


        
        if len(list_folders) > 0:
            max_folder = max(list_folders)
            new_folder = max_folder[-3:]
            folder_name = max_folder[:-3]
            number_up = int(new_folder) + 1
            new_number = format(number_up, '03')
            folder_up = folder_name + new_number
            
            new_save_dir = save_work_dir +'/'+ folder_up + '/'
            description = {'description': str(self.myWidget.textEdit_writeDescription.toPlainText()) }
            os.mkdir(new_save_dir)
            new_json_file = save_work_dir + '/' + folder_up
            to=new_save_dir+load_folder
            copytree(load_work_dir , to)
            
            with open(new_json_file + '.json', 'w') as outfile:
                json.dump(description, outfile)            
            
            with ZipFile(str(new_json_file) + '.zip', 'w') as self.myzip:
                [self.myzip.write(i) for i in [str(new_json_file) + '.json',str(save_work_dir)+'/readme.md']]
            #self.zipdir(str(save_work_dir) +'/' + folder_up + '/', self.myzip)    
        else:
            folder_up = load_folder + '_v001'
            new_save_dir = save_work_dir +'/'+ folder_up + '/'
            new_json_file = save_work_dir + '/' + folder_up
            description = {'description': str(self.myWidget.textEdit_writeDescription.toPlainText()) }
            os.mkdir(new_save_dir)
            to=new_save_dir+load_folder
            copytree(load_work_dir , to)
                        
            with open(new_json_file + '.json', 'w') as outfile:
                json.dump(description, outfile)
         
            with ZipFile(new_json_file+'.zip', 'w') as self.myzip:
                [self.myzip.write(i) for i in [str(new_json_file) + '.json',str(save_work_dir)+'/readme.md']]
            #self.zipdir(str(save_work_dir) +'/' + folder_up + '/', self.myzip)

        
        for path, subdirs, files in os.walk(str(save_work_dir) +'/' + folder_up ):
            #print path,subdirs, files, 'sdfsdff'
            for name in files:
                self.myzip.write( os.path.join(path, name))


        os.remove(save_work_dir+'/readme.md')
        self.myzip.close()
        #print 'done'
        
        self.checkArchives()
        
        self.myWidget.statusbar.showMessage('The work area has been saved to version: {}'.format(folder_up))


    def treeDir(self):
        
        model = QtGui.QFileSystemModel(self)
        # You can setRootPath to any path.
        model.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)
        drive = self.myWidget.lineEdit_loadWorkArea.text()
        model.setRootPath(drive)
        print model.rootPath()
        self.myWidget.treeView_folders.setModel(model)
        self.myWidget.treeView_folders.setRootIndex(model.index(drive))


    def storeWorkAreaDir(self):
        
        # load Qt file dialog for folder
        folder_path = QtGui.QFileDialog.getExistingDirectory(self,'Load folder path for work area directory')
        
        # set folder path
        self.myWidget.lineEdit_storeWorkArea.setText(folder_path)
        
        # print status folder
        self.myWidget.statusbar.showMessage('The Folder has been loaded')


    def loadWorkAreaDir(self):
        
        # load Qt file dialog for folder
        folder_path = QtGui.QFileDialog.getExistingDirectory(self,'Load folder path for store work area directory')
        
        # set folder path
        self.myWidget.lineEdit_loadWorkArea.setText(folder_path)
        
        #self.myWidget.treeWidget_folders.
        # print status folder
        self.treeDir()
        self.myWidget.statusbar.showMessage('The Folder has been loaded')

    def load_ui(self, ui_file, parent=None):
        # load window ui
        if run_modules == 'PySide':
            loader = QtUiTools.QUiLoader()
            file = QtCore.QFile(ui_file)
            file.open(QtCore.QFile.ReadOnly)
            myWidget = loader.load(file, None)
            file.close()
        else:
            myWidget = uic.loadUi(dir_path + "/" + ui_file)

        return myWidget

    def save_windows(self):
        # save window options
        qsettings = qt.QSettings(dir_path+ "/windows/settings.ini", qt.QSettings.IniFormat)

        qsettings.beginGroup("mainWindow")
        qsettings.setValue("geometry", self.myWidget.saveGeometry())
        qsettings.setValue("saveState", self.myWidget.saveState())
        qsettings.setValue("maximized", self.myWidget.isMaximized())
        qsettings.endGroup()

        print 'window saved'

    def restore_windows(self):
        # restore window option
        qsettings = qt.QSettings(dir_path+ "/windows/settings.ini", qt.QSettings.IniFormat)

        qsettings.beginGroup("mainWindow")

        self.myWidget.restoreGeometry(qsettings.value("geometry", "").toByteArray())
        self.myWidget.restoreState(qsettings.value("saveState", '').toByteArray())
        if qsettings.value("maximized", '').toPyObject() == 'true':
            self.myWidget.showMaximized()

        qsettings.endGroup()

        print 'window restored'


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    if run_modules == 'PySide':
        m = MyWidget()
        print "Showing"
        # ui = m#.show()
        print "Done"
        atexit.register(m.save_windows)
        m = app.exec_()
        print "Exec"
    else:
        m = MyWidget()
        m.myWidget.show()
        atexit.register(m.save_windows)
        sys.exit(app.exec_())









