from PyQt5.QtWidgets import QMessageBox

class CancelMessageBox(QMessageBox):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Interrompre l'analyse ?")
        self.setIcon(QMessageBox.Warning)

        self.setText("Êtes-vous sûr de vouloir interrompre l'analyse des images ?")
        self.setInformativeText("Cette analyse sera perdue et devra être recommencée depuis le début.")

        self._cancel_button = self.addButton("Interrompre", QMessageBox.DestructiveRole)
        self._continue_button = self.addButton("Reprendre", QMessageBox.RejectRole)
        self.setDefaultButton(self._continue_button)

    def exec_(self) -> bool:
        super().exec_()

        if self.clickedButton() == self._continue_button:
            return False
        elif self.clickedButton() == self._cancel_button:
            return True