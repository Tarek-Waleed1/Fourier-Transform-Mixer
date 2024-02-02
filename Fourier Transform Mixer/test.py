import sys
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        self.graphWidget.plot(hour, temperature)

        self.label = pg.TextItem(text="X: {} \nY: {}".format(0, 0))
        self.graphWidget.addItem(self.label)

        self.setMouseTracking(True)
        self.graphWidget.scene().sigMouseMoved.connect(self.onMouseMoved)
        self.graphWidget.scene().sigMouseClicked.connect(self.mouse_clicked)

    def onMouseMoved(self, evt):
        if self.graphWidget.plotItem.vb.mapSceneToView(evt):
            point = self.graphWidget.plotItem.vb.mapSceneToView(evt)
            self.label.setHtml(
                "<p style='color:white'>X： {0} <br> Y: {1}</p>". \
                    format(point.x(), point.y()))

    def mouse_clicked(self, evt):
        vb = self.graphWidget.plotItem.vb
        scene_coords = evt.scenePos()
        if self.graphWidget.sceneBoundingRect().contains(scene_coords):
            mouse_point = vb.mapSceneToView(scene_coords)
            print(f'clicked plot X: {mouse_point.x()}, Y: {mouse_point.y()}, event: {evt}')

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()