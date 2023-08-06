# Pyflow an open-source tool for modular visual programing in python
# Copyright (C) 2021-2022 Bycelium <https://www.gnu.org/licenses/>

""" Module for the handling of scene clipboard operations. """

from typing import TYPE_CHECKING, OrderedDict
from warnings import warn

import json
from PyQt5.QtWidgets import QApplication

from pyflow.core.edge import Edge

if TYPE_CHECKING:
    from pyflow.scene import Scene
    from pyflow.graphics.view import View


class SceneClipboard:

    """Helper object to handle clipboard operations on an Scene."""

    def __init__(self, scene: "Scene"):
        """Helper object to handle clipboard operations on an Scene.

        Args:
            scene: Scene reference.

        """
        self.scene = scene

    def cut(self):
        """Cut the selected items and put them into clipboard."""
        self._store(self._serializeSelected(delete=True))

    def copy(self):
        """Copy the selected items into clipboard."""
        self._store(self._serializeSelected(delete=False))

    def paste(self):
        """Paste the items in clipboard into the current scene."""
        self._deserializeData(self._gatherData())

    def _serializeSelected(self, delete=False) -> OrderedDict:
        selected_blocks, selected_edges = self.scene.sortedSelectedItems()
        selected_sockets = {}

        # Gather selected sockets
        for block in selected_blocks:
            for socket in block.sockets_in + block.sockets_out:
                selected_sockets[socket.id] = socket

        # Filter edges that are not fully connected to selected sockets
        for edge in selected_edges:
            if (
                edge.source_socket.id not in selected_sockets
                or edge.destination_socket.id not in selected_sockets
            ):
                selected_edges.remove(edge)

        data = OrderedDict(
            [
                ("blocks", [block.serialize() for block in selected_blocks]),
                ("edges", [edge.serialize() for edge in selected_edges]),
            ]
        )

        if delete:  # Remove selected items
            self.scene.views()[0].deleteSelected()

        return data

    def _find_bbox_center(self, blocks_data):
        xmin, xmax, ymin, ymax = 0, 0, 0, 0
        for block_data in blocks_data:
            x, y = block_data["position"]
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
        return (xmin + xmax) / 2, (ymin + ymax) / 2

    def _deserializeData(self, data: OrderedDict, set_selected=True):
        if data is None:
            return

        hashmap = {}

        view = self.scene.views()[0]
        mouse_pos = view.lastMousePos
        if set_selected:
            self.scene.clearSelection()

        # Finding pasting bbox center
        bbox_center_x, bbox_center_y = self._find_bbox_center(data["blocks"])
        offset_x, offset_y = (
            mouse_pos.x() - bbox_center_x,
            mouse_pos.y() - bbox_center_y,
        )

        # Create blocks
        for block_data in data["blocks"]:
            block = self.scene.create_block(block_data, hashmap, restore_id=False)
            if set_selected:
                block.setSelected(True)
            block.setPos(block.x() + offset_x, block.y() + offset_y)

        # Create edges
        for edge_data in data["edges"]:
            edge = Edge()
            edge.deserialize(edge_data, hashmap, restore_id=False)

            if set_selected:
                edge.setSelected(True)
            self.scene.addItem(edge)
            hashmap.update({edge_data["id"]: edge})

        self.scene.history.checkpoint(
            "Desiralized elements into scene", set_modified=True
        )

    def _store(self, data: OrderedDict):
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def _gatherData(self) -> str:
        str_data = QApplication.instance().clipboard().text()
        try:
            return json.loads(str_data)
        except ValueError as valueerror:
            warn(f"Clipboard text could not be loaded into json data: {valueerror}")
            return
