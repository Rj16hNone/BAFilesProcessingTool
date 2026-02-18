# coding: utf-8
import shutil
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from .obj_to_png import restore_tool, getAllFiles


class CraftThread(QThread):
    msgSignal = Signal(object)
    progressSignal = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}

    def run(self) -> None:
        meshPath = self.data.get('meshPath')
        texture2DPath = self.data.get('texture2DPath')
        savePath = self.data.get('savePath')

        png_list = getAllFiles(texture2DPath)
        length = len(png_list)

        for index, png_file in enumerate(png_list, 1):
            self.sleep(1)
            progress = index / length * 100
            self.progressSignal.emit(progress)
            self.msgSignal.emit(f'<span style="color:#4263eb">正在还原：{png_file}</span>')

            try:
                name = png_file.stem
                obj = Path(meshPath) / f'{name}-mesh.obj'
                save = Path(savePath) / f'{name}.png'

                if save.exists():
                    self.msgSignal.emit(f'<span style="color:yellow">{save} 已存在，跳过</span><br>')
                    continue
                if not obj.exists():
                    self.msgSignal.emit(
                        f'<span style="color:yellow">{png_file} 没有对应的 obj 文件，无需还原，复制到对应位置</span><br>')
                    shutil.copy(png_file, save)
                    continue
                restore_tool(obj, png_file, save)
                self.msgSignal.emit(f'<span style="color:green">还原成功：{save}</span><br>')
            except Exception as e:
                error = f'<span style="color:red">还原失败：{e}</span>'
                print(error)
                self.msgSignal.emit(error + '<br>')

    def setData(self, data: dict):
        self.data = data
        if not self.isRunning():
            self.start()
