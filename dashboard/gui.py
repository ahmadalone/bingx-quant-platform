import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit, QWidget
from PySide6.QtCore import Qt
import logging

logger = logging.getLogger(__name__)

class TradingDashboard(QMainWindow):
    """Professional Bloomberg-style GUI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BingX Quant Platform - Institutional Execution Desk")
        self.setGeometry(100, 100, 1600, 900)

        # Central area
        central = QWidget()
        self.setCentralWidget(central)

        # Log dock
        log_dock = QDockWidget("Logs & Live Data", self)
        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_dock.setWidget(log_text)
        self.addDockWidget(Qt.RightDockWidgetArea, log_dock)

        logger.info("GUI initialized with real-time capabilities.")

    def show(self):
        super().show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingDashboard()
    window.show()
    sys.exit(app.exec())