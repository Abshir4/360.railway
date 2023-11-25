import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF

class GraphicsView(QGraphicsView):
    def __init__(self, parent, colors, save_path, pixel_to_meter_scale):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.pixmapItem = QGraphicsPixmapItem()
        self.scene().addItem(self.pixmapItem)
        self.setSceneRect(self.pixmapItem.boundingRect())

        self.lines = []  # List to store drawn lines and their data
        self.colors = colors
        self.current_color_index = 0
        self.save_path = save_path
        self.pixel_to_meter_scale = pixel_to_meter_scale  # Scale factor to convert pixels to meters
        self.current_line = None  # Keep track of the current line

    def wheelEvent(self, event):
        zoom_factor = 1.05 if event.angleDelta().y() > 0 else 1 / 1.05
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = self.mapToScene(event.pos())
            if not self.current_line:
                self.current_line = [point]
            else:
                self.current_line.append(point)
                if len(self.current_line) >= 2:
                    self.lines.append({'coordinates': [(self.current_line[-2].x(), self.current_line[-2].y()), (point.x(), point.y())], 'distance': 0})
                    self.draw_measurement_line()
                self.change_color()

    def draw_measurement_line(self):
        pen = QPen(self.colors[self.current_color_index])
        pen.setWidthF(0.1)  # Adjust the line width for better precision
        line_data = self.lines[-1]
        line = QLineF(line_data['coordinates'][0][0], line_data['coordinates'][0][1], line_data['coordinates'][1][0], line_data['coordinates'][1][1])
        distance_pixels = line.length()  # Calculate the distance in pixels
        distance_meters = distance_pixels * self.pixel_to_meter_scale  # Convert to meters
        line_data['distance'] = round(distance_meters, 2)  # Update the distance
        self.scene().addLine(line, pen)
        self.display_coordinates(line, self.colors[self.current_color_index])

    def display_coordinates(self, line, color):
        x1, y1, x2, y2 = line.x1(), line.y1(), line.x2(), line.y2()
        distance = self.lines[-1]['distance']
        text = f"({x1:.4f}, {y1:.4f}) - ({x2:.4f}, {y2:.4f}, {distance:.2f} meters)"
        self.addTextItem(text, color, QPointF(x1, y1))

    def addTextItem(self, text, color, position):
        text_item = self.scene().addText(text)
        text_item.setDefaultTextColor(QColor(color))
        text_item.setPos(position)

    def change_color(self):
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)

    def save_to_json(self):
        data = [{'coordinates': line['coordinates'], 'distance': line['distance']} for line in self.lines]
        with open(self.save_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

class ImageViewer(QMainWindow):
    def __init__(self, image_path, colors, save_path, pixel_to_meter_scale):
        super().__init__()

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        self.setCentralWidget(main_widget)

        self.initUI(image_path, colors, save_path, pixel_to_meter_scale)

    def initUI(self, image_path, colors, save_path, pixel_to_meter_scale):
        self.view = GraphicsView(self, colors, save_path, pixel_to_meter_scale)
        self.centralWidget().layout().addWidget(self.view)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Viewer')

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        self.image_path = image_path

        if self.image_path:
            self.load_image()

        self.save_button = QPushButton("Save", self)
        self.save_button.setGeometry(10, 10, 100, 40)
        self.save_button.clicked.connect(self.view.save_to_json)

        self.show()

    def load_image(self):
        image = QPixmap(image_path)
        if not image.isNull():
            self.view.pixmapItem.setPixmap(image)
            self.view.setSceneRect(self.view.pixmapItem.boundingRect())

if __name__ == '__main__':
    image_path = "images/Boras-varberg-del2-end-section_012800.jpg"
    colors = [Qt.green, Qt.blue, Qt.red, Qt.cyan, Qt.magenta, Qt.yellow, Qt.black, Qt.darkCyan, Qt.darkMagenta, Qt.darkYellow]
    save_path = "output.json"
    pixel_to_meter_scale = 0.01

    app = QApplication(sys.argv)
    viewer = ImageViewer(image_path, colors, save_path, pixel_to_meter_scale)
    sys.exit(app.exec_())
