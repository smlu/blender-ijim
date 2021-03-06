from .key import *
from . import keyLoader
from ijim.model.utils import *
from ijim.utils.utils import *

import mathutils

import sys
import os.path
import time


def _set_obj_location(obj: bpy.types.Object, location: Vector3f):
    obj.location = location

    # Substract pivot offset from location
    for c in obj.constraints:
        if type(c) is bpy.types.PivotConstraint:
            pivot = -c.offset
            if c.target:
                pivot += -c.target.location
            obj.location += mathutils.Vector(pivot)
            break


def importKeyToScene(keyPath, scene: bpy.types.Scene):
    print("importing KEY: %r..." % (keyPath), end="")
    startTime = time.process_time ()

    key = keyLoader.load(keyPath)
    clearSceneAnimData(scene)

    scene.frame_start = 0
    scene.frame_end   = key.numFrames - 1
    scene.frame_step  = 1
    scene.render.fps  = key.fps
    scene.render.fps_base = 1.0

    scene.animation_flags = key.flags.name
    scene.animation_type  = key.type.name

    for m in key.markers:
        scene.timeline_markers.new(m.type.name, m.frame)

    for node in key.nodes:
        kobj = None

        # Get object to animate
        for obj in scene.objects:
            if kHnName in obj and obj[kHnName].lower() == node.meshName.lower():
                kobj = obj
                break
            elif node.meshName.lower() == obj.name.lower():
                kobj = obj
                break
            elif isOrderPrefixed(obj.name) and getOrderedNameIdx(obj.name) == node.num:
                kobj = obj
                break

        if kobj is None:
            raise ValueError("Cannot find object '{}' to animate!".format(node.meshName))

        # Set object's keyframes
        for keyframe in node.keyframes:
            _set_obj_location(kobj, keyframe.position)
            kobj.keyframe_insert(data_path="location", frame=keyframe.frame)

            setObjQuaternionRotation(kobj, keyframe.orientation)
            kobj.keyframe_insert(data_path="rotation_quaternion", frame=keyframe.frame)

    scene.frame_set(0)
    print(" done in %.4f sec." % (time.process_time() - startTime))
