import os
from cbook.model import helper, recipe_parser
from os.path import split
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap


class ReController:
    image = ""
    edit = False


    def __init__(self, model, window):
        self.model = model
        self.window = window

        self.window.btnAddIngredient.clicked.connect(self.add_ingredient_row)
        self.window.btnDeleteIngredient.clicked.connect(self.delete_ingredient_row)
        self.window.btnLoadImage.clicked.connect(self.open_select_image)
        self.window.btnDeleteImage.clicked.connect(self.delete_image)
        self.window.cbTags.activated.connect(self.activated_tags)
        self.window.btnClearTags.clicked.connect(self.clear_tags)
        self.window.btnReload.clicked.connect(self.reload)


    def reload(self):
        self.fill_data(self.recipe)


    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.window.lblRecipeImageEdit.setPixmap(pixmap)


    def prepare_tags(self, tags):
        self.window.cbTags.clear()
        self.window.cbTags.addItems(tags)


    def prepare_new(self, tags):
        self.edit = False
        self.prepare_tags(tags)
        self.window.leName.setText("")
        self.window.twIngredients.setRowCount(1)
        self.window.twIngredients.clearContents()
        self.set_image(self.window.get_default_meal_image_path())
        self.window.sbServingsEdit.setValue(4)
        self.window.btnReload.setHidden(True)
        self.clear_tags()
        self.window.teInstructions.setText("")
        self.window.teDescription.setText("")


    def fill_ingredients_table(self, ingredients):
        tableWidget = self.window.twIngredients
        tableWidget.setRowCount(len(ingredients))
        index = 0
        for i in ingredients:
            if len(i.split(';')) >= 3:
                item = QtWidgets.QTableWidgetItem(i.split(';')[0])
                tableWidget.setItem(index, 0, item)
                item = QtWidgets.QTableWidgetItem(i.split(';')[1])
                tableWidget.setItem(index, 1, item)
                item = QtWidgets.QTableWidgetItem(i.split(';')[2])
                tableWidget.setItem(index, 2, item)
            elif len(i.split(' ')) >= 3:
                item = QtWidgets.QTableWidgetItem(i.split(' ')[0])
                tableWidget.setItem(index, 0, item)
                item = QtWidgets.QTableWidgetItem(i.split(' ')[1])
                tableWidget.setItem(index, 1, item)
                ing = ""
                for e in i.split(' ')[2:]:
                    ing = ing + e + " "
                item = QtWidgets.QTableWidgetItem(ing[:-1])
                tableWidget.setItem(index, 2, item)
            index = index + 1


    def fill_data(self, recipe):
        rd = self.model.get_recipe_dict(recipe)
        self.window.leName.setText(self.model.get_name(rd))
        image_path = os.path.dirname(recipe) + "/full.jpg"
        if not os.path.exists(image_path):
            image_path = self.window.get_default_meal_image_path()
        self.set_image(image_path)
        self.window.sbServingsEdit.setValue(self.model.get_servings(rd))
        instructions = self.model.get_instructions(rd)
        text = ""
        for i in instructions:
            text = text + i + "\n\n"
        self.window.teInstructions.setText(text)
        self.window.teDescription.setText(self.model.get_description(rd))
        t = self.model.get_tags(rd)
        self.window.lblTagsEdit.setText(t)
        self.fill_ingredients_table(self.model.get_ingredients(rd))


    def prepare_edit(self, recipe, tags):
        self.edit = True
        self.recipe = recipe
        self.prepare_tags(tags)
        self.fill_data(recipe)


    def add_ingredient_row(self):
        tableWidget = self.window.twIngredients
        tableWidget.insertRow(tableWidget.rowCount())


    def delete_ingredient_row(self):
        tableWidget = self.window.twIngredients
        tableWidget.removeRow(tableWidget.rowCount()-1)


    def open_select_image(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self.window, 
                'Öffne Bild', 
                '',
                "Image files (*.jpg *.gif *.png *.jpeg *.svg)")
        if fname:
            self.image = fname
            self.set_image(fname)


    def delete_image(self):
        self.image = ""
        self.set_image(self.window.get_default_meal_image_path())


    def activated_tags(self):
        selected = self.window.cbTags.currentText()
        # add to list
        text = self.window.lblTagsEdit.text()
        if selected not in text.split(','):
            if text != "":
                text = text + ","
            self.window.lblTagsEdit.setText(text + selected)
            # clear comboBox
            self.window.cbTags.clearEditText()


    def clear_tags(self):
        self.window.lblTagsEdit.setText("")


    def get_ingredients(self):
        ingredients = []
        model = self.window.twIngredients.model()
        for r in range(0,self.window.twIngredients.rowCount()):
            ingredient = []
            menge = model.data(model.index(r, 0))
            einheit = model.data(model.index(r, 1))
            zutat = model.data(model.index(r, 2))
            if menge or einheit or zutat:
                if menge:
                    menge = menge.replace(",",".")
                    try:
                        menge = helper.string_to_float(menge)
                    except:
                        QtWidgets.QMessageBox.critical(self.window, "Ungültige Mengenangabe",
                                "Ungültige Mengeneingabe '" + str(menge) + "'.\n" +
                                "Entweder als Dezimalzahl (z.B. '1.5')\n" +
                                "oder als Bruch (z.B. '1 1/2' oder '3/5') eingeben!")
                        return None
                else:
                    menge = ""
                if not einheit:
                    einheit = ""
                else:
                    einheit = einheit.replace(" ","")
                if not zutat:
                    QtWidgets.QMessageBox.critical(self.window, "Ungültige Zutatenangabe",
                            "Leeres Zutatenfeld!")
                    return None

                ingredients.append(str(menge) + " " + str(einheit) + " " + str(zutat))
            else:
                print("Skipped empty ingredient row")
        if not ingredients:
            QtWidgets.QMessageBox.critical(self.window, "Ungültige Zutaten",
                    "Keine Zutaten angegeben!")
        return ingredients


    def save_recipe(self):
        name = self.window.leName.text()
        if self.edit or self.model.check_name(name):
            ingredients = self.get_ingredients()
            if ingredients:
                # read recipe data and save recipe
                portionen = self.window.sbServingsEdit.value()
                anleitung = self.window.teInstructions.toPlainText()
                beschreibung = self.window.teDescription.toPlainText()
                tags = self.window.lblTagsEdit.text()
                
                self.model.save_recipe(name, self.image, ingredients, portionen,
                        beschreibung, anleitung, tags)

                # prevent having two folders with the same recipe
                if self.edit:
                    rd = self.model.get_recipe_dict(self.recipe)
                    if name != self.model.get_name(rd):
                        self.model.delete_recipe(self.recipe)

                return True
            else:
                return False
        else:
            QtWidgets.QMessageBox.critical(self.window, "Ungültiger Rezeptname",
                    "Ein Rezept mit diesem Namen ist bereits vorhanden.\n" +
                    "Bitte wähle einen anderen Namen!")
            return False
