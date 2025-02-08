import pymel.core as pm
import importlib

def onMayaDroppedPythonFile(*args, **kwargs):
    current_shelf = pm.mel.eval("shelfTabLayout -query -selectTab $gShelfTopLevel")

    pm.shelfButton(
        i='MS_shotSculptor_Icon.png',
        p=current_shelf,
        sourceType='python',
        label='MS-Shot-Sculptor',
        c="import importlib; import MS_ShotSculptor_PY3; importlib.reload(MS_ShotSculptor_PY3)",
        ann="Open MS-Shot-Sculptor"
    )