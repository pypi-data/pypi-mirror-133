from __future__ import nested_scopes
from collections import namedtuple
from dataclasses import dataclass
from typing import Union

from aoc import Point


@dataclass
class Rect:
    """
    Rect class (x,y) with width and height all inclusive
    """
    x: int
    y: int
    w: int
    h: int

    def contains_point(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def points(self):
        for y in range(self.y, self.y + self.h):
            for x in range(self.x, self.x + self.w):
                yield (x, y)

    def contains(self, other):
        return self.x <= other.x and self.y <= other.y and self.x + self.w >= other.x + other.w and self.y + self.h >= other.y + other.h and self.x + self.w > other.x and self.y + self.h > other.y

    def intersection(self, other):
        x = y = w = h = None

        # Left
        if other.x <= self.x < other.x + other.w:
            x = self.x
        elif self.x <= other.x < self.x + self.w:
            x = other.x
        else:
            return None

        # Right
        if self.x + self.w > other.x and self.x + self.w <= other.x + other.w:
            w = self.x + self.w - x
        elif other.x + other.w > self.x and other.x + other.w <= self.x + self.w:
            w = other.x + other.w - x
        else:
            return None

        # Top
        if self.y >= other.y and self.y < other.y + other.h:
            y = self.y
        elif other.y >= self.y and other.y < self.y + self.h:
            y = other.y
        else:
            return None

        # Bottom
        if self.y + self.h > other.y and self.y + self.h <= other.y + other.h:
            h = self.y + self.h - y
        elif other.y + other.h > self.y and other.y + other.h <= self.y + self.h:
            h = other.y + other.h - y
        else:
            return None
        return Rect(x, y, w, h)
