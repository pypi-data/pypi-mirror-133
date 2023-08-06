# Pyflow an open-source tool for modular visual programing in python
# Copyright (C) 2021-2022 Bycelium <https://www.gnu.org/licenses/>

""" Module for the base Scene."""

import math
import json
from os import path
from types import FunctionType, ModuleType
from typing import List, OrderedDict, Union

from PyQt5.QtCore import QLine, QRectF, QThreadPool
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsScene

from pyflow.core.serializable import Serializable
from pyflow.blocks.block import Block
from pyflow.core.edge import Edge
from pyflow.scene.clipboard import SceneClipboard
from pyflow.scene.history import SceneHistory
from pyflow.core.kernel import Kernel
from pyflow.scene.from_ipynb_conversion import ipynb_to_ipyg
from pyflow.scene.to_ipynb_conversion import ipyg_to_ipynb
from pyflow import blocks


class Scene(QGraphicsScene, Serializable):

    """Scene for the  Window."""

    def __init__(
        self,
        parent=None,
        background_color: str = "#393939",
        grid_color: str = "#292929",
        grid_light_color: str = "#2f2f2f",
        width: int = 64000,
        height: int = 64000,
        grid_size: int = 20,
        grid_squares: int = 5,
    ):
        Serializable.__init__(self)
        QGraphicsScene.__init__(self, parent=parent)

        self._background_color = QColor(background_color)
        self._grid_color = QColor(grid_color)
        self._grid_light_color = QColor(grid_light_color)
        self.grid_size = grid_size
        self.grid_squares = grid_squares

        self.width, self.height = width, height
        self.setSceneRect(-self.width // 2, -self.height // 2, self.width, self.height)
        self.setBackgroundBrush(self._background_color)

        self._has_been_modified = False
        self._has_been_modified_listeners = []

        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

        self.kernel = Kernel()
        self.threadpool = QThreadPool()

    @property
    def has_been_modified(self):
        """True if the scene has been modified, False otherwise."""
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value: bool):
        self._has_been_modified = value
        for callback in self._has_been_modified_listeners:
            callback()

    def addHasBeenModifiedListener(self, callback: FunctionType):
        """Add a callback that will trigger when the scene has been modified."""
        self._has_been_modified_listeners.append(callback)

    def sortedSelectedItems(self) -> List[Union[Block, Edge]]:
        """Returns the selected blocks and selected edges in two separate lists."""
        selected_blocks, selected_edges = [], []
        for item in self.selectedItems():
            if isinstance(item, Block):
                selected_blocks.append(item)
            if isinstance(item, Edge):
                selected_edges.append(item)
        return selected_blocks, selected_edges

    def drawBackground(self, painter: QPainter, rect: QRectF):
        """Draw the Scene background."""
        super().drawBackground(painter, rect)
        self.drawGrid(painter, rect)

    def drawGrid(self, painter: QPainter, rect: QRectF):
        """Draw the background grid."""
        left = int(math.floor(rect.left()))
        top = int(math.floor(rect.top()))
        right = int(math.ceil(rect.right()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        # Compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # Draw the lines using the painter
        pen = QPen(self._grid_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLines(*lines_dark)

        pen = QPen(self._grid_light_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLines(*lines_light)

    def save(self, filepath: str):
        """Save the scene into filepath."""
        self.save_to_ipyg(filepath)
        self.has_been_modified = False

    def save_to_ipyg(self, filepath: str):
        """Save the scene into filepath as interactive python graph (.ipyg)."""
        if "." not in filepath:
            filepath += ".ipyg"

        extention_format = filepath.split(".")[-1]
        if extention_format != "ipyg":
            raise NotImplementedError(f"Unsupported format {extention_format}")

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.serialize(), indent=4))

    def save_to_ipynb(self, filepath: str):
        """Save the scene into filepath as ipynb."""
        if "." not in filepath:
            filepath += ".ipynb"

        extention_format: str = filepath.split(".")[-1]
        if extention_format != "ipynb":
            raise NotImplementedError(
                f"The file should be a *.ipynb (not a .{extention_format})"
            )

        with open(filepath, "w", encoding="utf-8") as file:
            json_ipyg_data: OrderedDict = self.serialize()
            json_ipynb_data: OrderedDict = ipyg_to_ipynb(json_ipyg_data)
            file.write(json.dumps(json_ipynb_data, indent=4))

    def load(self, filepath: str):
        """Load a saved scene.

        Args:
            filepath: Path to the file to load.

        """
        if filepath.endswith(".ipyg"):
            data = self.load_from_json(filepath)
        elif filepath.endswith(".ipynb"):
            ipynb_data = self.load_from_json(filepath)
            data = ipynb_to_ipyg(ipynb_data)
        else:
            extention_format = filepath.split(".")[-1]
            raise NotImplementedError(f"Unsupported format {extention_format}")
        self.deserialize(data)
        self.history.checkpoint("Loaded scene")
        self.has_been_modified = False

        # Add filepath to kernel path
        dir_path = repr(path.abspath(path.dirname(filepath)))
        setup_path_code = f'__import__("os").chdir({dir_path})'
        self.kernel.execute(setup_path_code)

    def load_from_json(self, filepath: str) -> OrderedDict:
        """
        Load the json data into an ordered dict

        Args:
            filepath: Path to the file to load.
        """
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
        return data

    def clear(self):
        """Clear the scene from all items."""
        self.has_been_modified = False
        return super().clear()

    def serialize(self) -> OrderedDict:
        """Serialize the scene into a dict."""
        blocks = []
        edges = []
        for item in self.items():
            if isinstance(item, Block):
                blocks.append(item)
            elif isinstance(item, Edge):
                edges.append(item)
        blocks.sort(key=lambda x: x.id)
        edges.sort(key=lambda x: x.id)
        return OrderedDict(
            [
                ("id", self.id),
                ("blocks", [block.serialize() for block in blocks]),
                ("edges", [edge.serialize() for edge in edges]),
            ]
        )

    def create_block_from_file(self, filepath: str, x: float = 0, y: float = 0):
        """Create a new block from a .b file."""
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            data["position"] = [x, y]
            data["sockets"] = {}
            self.create_block(data, None, False)

    def create_block(
        self, data: OrderedDict, hashmap: dict = None, restore_id: bool = True
    ) -> Block:
        """Create a new block from an OrderedDict."""

        block = None

        block_constructor = None
        block_files = blocks.__dict__

        for block_name in block_files:
            block_module = getattr(blocks, block_name)
            if isinstance(block_module, ModuleType):
                if hasattr(block_module, data["block_type"]):
                    block_constructor = getattr(blocks, data["block_type"])

        if block_constructor is None:
            raise NotImplementedError(f"{data['block_type']} is not a known block type")

        block = block_constructor()
        block.deserialize(data, hashmap, restore_id)
        self.addItem(block)
        if hashmap is not None:
            hashmap.update({data["id"]: block})
        return block

    def deserialize(
        self, data: OrderedDict, hashmap: dict = None, restore_id: bool = True
    ):
        self.clear()
        hashmap = hashmap if hashmap is not None else {}
        if restore_id and "id" in data:
            self.id = data["id"]

        # Create blocks
        for block_data in data["blocks"]:
            self.create_block(block_data, hashmap, restore_id)

        # Create edges
        for edge_data in data["edges"]:
            edge = Edge()
            edge.deserialize(edge_data, hashmap, restore_id)
            self.addItem(edge)
            hashmap.update({edge_data["id"]: edge})
