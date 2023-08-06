# Pyflow an open-source tool for modular visual programing in python
# Copyright (C) 2021-2022 Bycelium <https://www.gnu.org/licenses/>

""" Module for the base Edge."""

from __future__ import annotations

from typing import Optional, OrderedDict

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import (
    QGraphicsPathItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

from pyflow.core.serializable import Serializable
from pyflow.core.socket import Socket


class Edge(QGraphicsPathItem, Serializable):

    """Base class for directed edges in Pyflow."""

    DEFAULT_DATA = {"path_type": "bezier"}
    MANDATORY_FIELDS = {"source", "destination"}

    def __init__(
        self,
        edge_width: float = 4.0,
        path_type=DEFAULT_DATA["path_type"],
        edge_color="#001000",
        edge_selected_color="#00ff00",
        edge_running_color="#FF0000",
        edge_transmitting_color="#00ff00",
        source: QPointF = QPointF(0, 0),
        destination: QPointF = QPointF(0, 0),
        source_socket: Socket = None,
        destination_socket: Socket = None,
    ):
        """Base class for edges in Pyflow.

        Args:
            edge_width: Width of the edge.
            path_type: Type of path, one of ('direct', 'bezier').
            edge_color: Color of the edge.
            edge_selected_color: Color of the edge when it is selected.
            source: Source point of the directed edge.
            destination: Destination point of the directed edge.
            source_socket: Source socket of the directed edge, overrides source.
            destination_socket: Destination socket of the directed edge, overrides destination.

        """

        Serializable.__init__(self)
        QGraphicsPathItem.__init__(self, parent=None)
        self._pen = QPen(QColor(edge_color))
        self._pen.setWidthF(edge_width)

        self._pen_dragging = QPen(QColor(edge_color))
        self._pen_dragging.setWidthF(edge_width)
        self._pen_dragging.setStyle(Qt.PenStyle.DashLine)

        self._pen_selected = QPen(QColor(edge_selected_color))
        self._pen_selected.setWidthF(edge_width)

        self._pen_running = QPen(QColor(edge_running_color))
        self._pen_running.setWidthF(edge_width)

        self._pen_transmitting = QPen(QColor(edge_transmitting_color))
        self._pen_transmitting.setWidthF(edge_width)

        self.pens = [self._pen, self._pen_running, self._pen_transmitting]

        # 0 for normal, 1 for running, 2 for transmitting
        self.run_state = 0

        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(-1)

        self.path_type = path_type

        self.source_socket = source_socket
        self.destination_socket = destination_socket

        self._source = source
        self._destination = destination
        self.update_path()

    def remove_from_socket(self, socket_type="source"):
        """Remove the edge from the sockets it is snaped to on the given socket_type.

        Args:
            socket_type: One of ('source', 'destination').

        """
        socket_name = f"{socket_type}_socket"
        socket = getattr(self, socket_name, Socket)
        if socket is not None:
            socket.remove_edge(self)
            setattr(self, socket_name, None)

    def remove_from_sockets(self):
        """Remove the edge from all sockets it is snaped to."""
        self.remove_from_socket("source")
        self.remove_from_socket("destination")

    def remove(self):
        """Remove the edge from the scene in which it is drawn."""
        scene = self.scene()
        if scene is not None:
            self.remove_from_sockets()
            scene.removeItem(self)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,  # pylint:disable=unused-argument
        widget: Optional[QWidget] = None,
    ):  # pylint:disable=unused-argument
        """Paint the edge."""
        self.update_path()
        if self.isSelected():
            pen = self._pen_selected
        elif self.destination_socket is None:
            pen = self._pen_dragging
        else:
            pen = self.pens[self.run_state]
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())

    def update_path(self):
        """Update the edge path depending on the path_type."""
        path = QPainterPath(self.source)
        if self.path_type == "direct":
            path.lineTo(self.destination)
        elif self.path_type == "bezier":
            sx, sy = self.source.x(), self.source.y()
            dx, dy = self.destination.x(), self.destination.y()
            mid_dist = (dx - sx) / 2
            path.cubicTo(sx + mid_dist, sy, dx - mid_dist, dy, dx, dy)
        else:
            raise NotImplementedError(f"Unknowed path type: {self.path_type}")
        self.setPath(path)

    @property
    def source(self) -> QPointF:
        """Source point of the directed edge."""
        if self.source_socket is not None:
            return self.source_socket.scenePos()
        return self._source

    @source.setter
    def source(self, value: QPointF):
        self._source = value
        try:
            self.update_path()
        except AttributeError:
            pass

    @property
    def source_socket(self) -> Socket:
        """Source socket of the directed edge."""
        return self._source_socket

    @source_socket.setter
    def source_socket(self, value: Socket):
        self._source_socket = value
        if value is not None:
            self.source_socket.add_edge(self, is_destination=False)
            self.source = value.scenePos()

    @property
    def destination(self) -> QPointF:
        """Destination point of the directed edge."""
        if self.destination_socket is not None:
            return self.destination_socket.scenePos()
        return self._destination

    @destination.setter
    def destination(self, value: QPointF):
        self._destination = value
        try:
            self.update_path()
        except AttributeError:
            pass

    @property
    def destination_socket(self) -> Socket:
        """Destination socket of the directed edge."""
        return self._destination_socket

    @destination_socket.setter
    def destination_socket(self, value: Socket):
        self._destination_socket = value
        if value is not None:
            self.destination_socket.add_edge(self, is_destination=True)
            self.destination = value.scenePos()

    def serialize(self) -> OrderedDict:
        return OrderedDict(
            [
                ("id", self.id),
                ("path_type", self.path_type),
                (
                    "source",
                    OrderedDict(
                        [
                            (
                                "block",
                                self.source_socket.block.id
                                if self.source_socket
                                else None,
                            ),
                            (
                                "socket",
                                self.source_socket.id if self.source_socket else None,
                            ),
                        ]
                    ),
                ),
                (
                    "destination",
                    OrderedDict(
                        [
                            (
                                "block",
                                self.destination_socket.block.id
                                if self.destination_socket
                                else None,
                            ),
                            (
                                "socket",
                                self.destination_socket.id
                                if self.destination_socket
                                else None,
                            ),
                        ]
                    ),
                ),
            ]
        )

    def deserialize(self, data: OrderedDict, hashmap: dict = None, restore_id=True):
        if restore_id and "id" in data:
            self.id = data["id"]

        self.complete_with_default(data)

        self.path_type = data["path_type"]
        try:
            self.source_socket = hashmap[data["source"]["socket"]]

            self.destination_socket = hashmap[data["destination"]["socket"]]
            self.update_path()
        except KeyError:
            self.remove()

    @property
    def run_state(self) -> int:
        """Run state.

        Describe the current state of the Edge:
            - 0: idle.
            - 1: running.
            - 2: transmitting.

        """
        return self._run_state

    @run_state.setter
    def run_state(self, value: int):
        self._run_state = value
        # Update to force repaint
        self.update()
