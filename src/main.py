from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.database.models import init_db, Base, engine
import sys

def main():
    # Initialize database and create tables
    Base.metadata.create_all(engine)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 