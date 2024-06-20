# Misc_steg_tool插件开发指南

请参考`plugin_model.py`内的编写插件，从而使主程序能成功读取

开发时需填写好插件名

```python
NAME = "PLUGIN_NAME"
```

以及插件的ui路径

```python
UI_PATH = os.path.join(getCurrentPath(), "PLUGIN_UI_PATH")
```

以便主程序可以读取

```python
PLUGIN_PATH = getCurrentPath() + "/" + "plugins"
```

加载插件的逻辑如下：

```python
def initPlugin(self):
        pluginsDirName = self.PLUGIN_PATH.split("/")[-1]
        fileNames = os.listdir(self.PLUGIN_PATH)
        # 將plugins目錄添加到sys.path, 防止在插件中出現ImportError
        pluginsPath = os.path.join(getCurrentPath(), "plugins")
        sys.path.append(pluginsPath)

        for fileName in fileNames:
            if fileName.endswith(".py"):
                self.loadPlugin(f"{pluginsDirName}.{fileName.split('.')[0]}")


def loadPlugin(self, pluginName):
    # filePath, _ = QFileDialog.getOpenFileName(self, "Select Plugin", filter="Python Files (*.py)")
    # # 獲取.py文件名
    # pluginName = filePath.split("/")[-1].split(".")[0]
    # 防止重複添加
    if self.importPlugins.get(pluginName) != None:
        QMessageBox.warning(self, "警告", f"{pluginName}插件已被加載，請勿重複添加!!!")
        return
    self.importPlugins[pluginName] = True
    # py動態加載模塊的方式
    module = import_module(pluginName)
    # 獲取模塊的Ui
    moduleUI = module.Ui()
    
    # 保存插件的signal, 用於兩者之間的信息傳遞
    self.signals[pluginName] = moduleUI.signal
    print(f"loading plugin: {pluginName}")
    # 添加到Tab中
    self.ui.Tab.addTab(moduleUI, moduleUI.NAME)
```

