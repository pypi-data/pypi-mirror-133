from cbook.model import helper
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QStyle, QToolButton
import os, sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



class MainWindow(QMainWindow):
    recipe_buttons = []


    def __init__(self):
        super(MainWindow, self).__init__()
        ui_file = resource_path("main_window.ui")
        uic.loadUi(ui_file, self)
        self.set_icons()


    def set_icons(self):
        self.btnDelete.setIcon(self.get_icon('edit-delete', QStyle.SP_TrashIcon))
        self.btnEdit.setIcon(self.get_icon('edit', QStyle.SP_ArrowForward))
        self.btnBack.setIcon(self.get_icon('go-previous', QStyle.SP_ArrowBack))
        self.btnSave.setIcon(self.get_icon('document-save', QStyle.SP_DialogSaveButton))
        self.btnReload.setIcon(self.get_icon('edit-clear', QStyle.SP_BrowserReload))
        self.btnCancel.setIcon(self.get_icon('edit-clear-all', QStyle.SP_DialogCancelButton))
        self.btnDeleteImage.setIcon(self.get_icon('edit-delete', QStyle.SP_DialogDiscardButton))
        self.btnClearTags.setIcon(self.get_icon('edit-delete', QStyle.SP_DialogDiscardButton))
        self.btnLoadImage.setIcon(self.get_icon('document-open', QStyle.SP_FileDialogStart))
        self.btnRecipeDir.setIcon(self.get_icon('folder', QStyle.SP_DirIcon))
        self.btnNewRecipe.setIcon(self.get_icon('document-new', QStyle.SP_FileIcon))
        self.btnAddIngredient.setIcon(self.get_icon('list-add', QStyle.SP_ArrowDown))
        self.btnDeleteIngredient.setIcon(self.get_icon('list-remove', QStyle.SP_ArrowUp))


    def add_recipe(self, recipe_button):
        self.recipe_buttons.append(recipe_button)
        layout = self.lhRecipeList.layout()
        layout.insertWidget(layout.count()-1,recipe_button)


    def get_recipe_buttons(self):
        return self.recipe_buttons


    def delete_recipe_buttons(self):
        layout = self.lhRecipeList.layout()
        helper.clear_layout(layout)
        self.recipe_buttons.clear()


    def set_image(self, image_path):
        if not os.path.exists(image_path):
            image_path = self.get_default_meal_image_path()
        pixmap = QPixmap(image_path)
        self.lblRecipeImage.setPixmap(pixmap)

        self.lblRecipeImage.resize(pixmap.width(),pixmap.height())


    def get_icon(self, theme_icon, fallback_icon):
        if QIcon.hasThemeIcon(theme_icon):
            return QIcon.fromTheme(theme_icon)
        else:
            # return default qt icon (fallback_icon)
            return self.style().standardIcon(fallback_icon)


    def get_default_meal_image_path(self):
        return resource_path("meal_icon.svg")
