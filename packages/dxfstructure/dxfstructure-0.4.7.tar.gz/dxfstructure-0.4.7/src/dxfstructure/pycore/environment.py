'''
--------------------------------------------------------------------------
Copyright (C) 2017-2018 Lukasz Laba <lukaszlab@o2.pl>

This file is part of DxfStructure (structural engineering dxf drawing system).

DxfStructure is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

DxfStructure is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

from dxfstructure.pycore.Bar import Bar
from dxfstructure.pycore.ConcreteModel import ConcreteModel
from dxfstructure.pycore.SteelModel import SteelModel
from dxfstructure.pycore.Drawing import Drawing
from dxfstructure.pycore.Creator import Creator
from dxfstructure.pycore.Checker import Checker
from dxfstructure.pycore.Schedule import Schedule
from dxfstructure.pycore.Executor import Executor
from dxfstructure.pycore.Scaner import Scaner

DRAWING = Drawing()
#---
CONCRETE_MODEL = ConcreteModel()
STEEL_MODEL = SteelModel()
#---
CREATOR =  Creator()
CREATOR.asign_Drawing(DRAWING)
#---
CHECKER = Checker()
CHECKER.asign_ConcreteModel(CONCRETE_MODEL)
CHECKER.asign_SteelModel(STEEL_MODEL)
CHECKER.asign_Drawing(DRAWING)
#---
SCHEDULE = Schedule()
SCHEDULE.asign_ConcreteModel(CONCRETE_MODEL)
SCHEDULE.asign_SteelModel(STEEL_MODEL)
SCHEDULE.asign_Drawing(DRAWING)
#---
EXECUTOR = Executor()
EXECUTOR.asign_Creator(CREATOR)
#---
SCANER = Scaner()
SCANER.asign_ConcreteModel(CONCRETE_MODEL)
SCANER.asign_SteelModel(STEEL_MODEL)
SCANER.asign_Drawing(DRAWING)
SCANER.asign_Executor(EXECUTOR)


