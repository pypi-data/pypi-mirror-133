#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
枚举
"""
from enum import Enum

__all__ = ['Action']

class Action(Enum):
    STORE = 'store'
    STORE_TRUE = 'store_true'
    APPEND = 'append'

