import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import re


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Plotter")
        self.setMinimumWidth(400)

        # Create main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create function input label and line edit
        self.function_label = QLabel("Enter a function of x (e.g., 5*x^3 + 2*x):")
        self.function_edit = QLineEdit()
        self.layout.addWidget(self.function_label)
        self.layout.addWidget(self.function_edit)

        # Create x range input labels and line edits
        self.x_min_label = QLabel("Min x:")
        self.x_max_label = QLabel("Max x:")
        self.x_min_edit = QLineEdit()
        self.x_max_edit = QLineEdit()
        self.layout.addWidget(self.x_min_label)
        self.layout.addWidget(self.x_min_edit)
        self.layout.addWidget(self.x_max_label)
        self.layout.addWidget(self.x_max_edit)

        # Create plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot)
        self.layout.addWidget(self.plot_button)

        # Create matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def plot(self):
        # Get user inputs
        function = self.function_edit.text()
        x_min = self.x_min_edit.text()
        x_max = self.x_max_edit.text()

        # Validate inputs
        if not function:
            self.show_message("Error", "Please enter a function.")
            return

        if not x_min or not x_max:
            self.show_message("Error", "Please enter both min and max values of x.")
            return

        try:
            x_min = float(x_min)
            x_max = float(x_max)
        except ValueError:
            self.show_message("Error", "Invalid min/max values of x.")
            return

        if x_min >= x_max:
            self.show_message("Error", "Max value of x must be greater than min value of x.")
            return

        # Parse and evaluate the function
        try:
            x = np.linspace(x_min, x_max, 500)
            y = eval(self.parse_function(function))
        except:
            self.show_message("Error", "Invalid function.")
            return

        # Clear the previous plot
        self.figure.clear()

        # Create a subplot and plot the function
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)

        # Refresh the canvas
        self.canvas.draw()

    def parse_function(self, function):
        # Replace ^ with **
        function = re.sub(r'\^', r'**', function)

        # Replace x with np.linspace(x_min, x_max, 500)
        function = re.sub(r'x', r'x_vals', function)

        return function

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
