# ==============================================================================
# FreeCAD Python Macro: NR-AGR-001_Composter_Johnson_v1
# Описание: Автоматическая генерация параметрической 3D-модели компостера
# Инструкция: 
#   1. Откройте FreeCAD
#   2. Перейдите в меню: View -> Panels -> Python Console
#   3. Скопируйте весь этот код и вставьте в консоль
#   4. Нажмите Enter. Модель будет построена автоматически.
# ==============================================================================

import FreeCAD
import Part

# 1. Создание нового документа
doc = FreeCAD.newDocument("NR-AGR-001_Composter_Johnson")

# 2. Параметрические размеры (в мм)
W = 1000  # Общая ширина
D = 1000  # Общая глубина
H = 1200  # Общая высота
T = 25    # Толщина доски

# 3. Функция создания панели с вентиляционными отверстиями
def create_ventilated_panel(width, height, depth, x, y, z, rot_y=0):
    # Базовый параллелепипед
    box = Part.makeBox(width, depth, height)
    
    # Вырезаем 4 отверстия диаметром 20 мм (радиус 10 мм)
    hole_heights = [200, 400, 600, 800]
    for h_y in hole_heights:
        # Цилиндр для булевой операции вырезания
        hole = Part.makeCylinder(10, depth, FreeCAD.Vector(width/2, 0, h_y))
        box = box.cut(hole)
    
    # Создание объекта в дереве документа FreeCAD
    obj = doc.addObject("Part::Feature", "Panel")
    obj.Shape = box
    obj.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, rot_y, 0))
    return obj

# 4. Генерация компонентов

# Задняя стенка
back = create_ventilated_panel(W, H, T, 0, 0, 0, 0)
back.Label = "01_Back_Panel"
back.ViewObject.ShapeColor = (0.6, 0.4, 0.2) # Цвет дерева

# Передняя стенка
front = create_ventilated_panel(W, H, T, 0, D-T, 0, 0)
front.Label = "02_Front_Panel"
front.ViewObject.ShapeColor = (0.6, 0.4, 0.2)

# Левая стенка (ширина = глубине компостера, глубина = толщине доски)
left_box = Part.makeBox(D, T, H)
for h_y in [200, 400, 600, 800]:
    hole = Part.makeCylinder(10, T, FreeCAD.Vector(D/2, 0, h_y))
    left_box = left_box.cut(hole)
left = doc.addObject("Part::Feature", "03_Left_Panel")
left.Shape = left_box
left.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0))
left.ViewObject.ShapeColor = (0.6, 0.4, 0.2)

# Правая стенка
right_box = Part.makeBox(D, T, H)
for h_y in [200, 400, 600, 800]:
    hole = Part.makeCylinder(10, T, FreeCAD.Vector(D/2, 0, h_y))
    right_box = right_box.cut(hole)
right = doc.addObject("Part::Feature", "04_Right_Panel")
right.Shape = right_box
right.Placement = FreeCAD.Placement(FreeCAD.Vector(W-T, 0, 0), FreeCAD.Rotation(0, 0, 0))
right.ViewObject.ShapeColor = (0.6, 0.4, 0.2)

# Внутренние перегородки (делят компостер на 3 равные секции по ~333 мм)
# Перегородка 1
div1_box = Part.makeBox(T, D, H)
div1 = doc.addObject("Part::Feature", "05_Divider_1")
div1.Shape = div1_box
div1.Placement = FreeCAD.Placement(FreeCAD.Vector(333, 0, 0), FreeCAD.Rotation(0, 0, 0))
div1.ViewObject.ShapeColor = (0.5, 0.35, 0.15)

# Перегородка 2
div2_box = Part.makeBox(T, D, H)
div2 = doc.addObject("Part::Feature", "06_Divider_2")
div2.Shape = div2_box
div2.Placement = FreeCAD.Placement(FreeCAD.Vector(666, 0, 0), FreeCAD.Rotation(0, 0, 0))
div2.ViewObject.ShapeColor = (0.5, 0.35, 0.15)

# 5. Финализация
doc.Label = "NR-AGR-001_Composter_Johnson_v1"
doc.recompute()
FreeCADGui.SendMsgToActiveView("ViewFit") # Автоматически вписать модель в экран

print("✅ Модель NR-AGR-001 успешно построена в FreeCAD!")
print("💡 Совет: Теперь вы можете экспортировать её: File -> Export -> STEP или STL")
