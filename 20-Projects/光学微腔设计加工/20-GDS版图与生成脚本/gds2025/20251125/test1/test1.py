# -*- coding: utf-8 -*-
import os.path
import gdsCAD as core
# 新增：导入 matplotlib.pyplot（必须在调用 show() 之前）

#Create two copies of the Cell
top =core.Cell('TOP')
cell_array=core.CellArray(cell,1,2,(0,850))
top.add(cell_array)
# Add the copied cell to a Layout and save
layout = core.Layout('LIBRARY')
layout.add(top)
layout.save('output.gds')
