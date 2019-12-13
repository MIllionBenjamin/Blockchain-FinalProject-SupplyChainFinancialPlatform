'''
  bcosliteclientpy is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/)
  bcosliteclientpy is free software: you can redistribute it and/or modify it under the
  terms of the MIT License as published by the Free Software Foundation. This project is
  distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Thanks for
  authors and contributors of eth-abi, eth-account, eth-hash，eth-keys, eth-typing, eth-utils,
  rlp, eth-rlp , hexbytes ... and relative projects
  @file: condition.py
  @function:
  @author: yujiechen
  @date: 2019-07
'''


class ConditionOp:
    """
    define operations for condition
    """
    _EQ_ = 0
    _NE_ = 1
    _GT_ = 2
    _GE_ = 3
    _LT_ = 4
    _LE_ = 5
    _LIMIT_ = 6


class Condition:
    """
    implementation of Condition
    """

    def __init__(self):
        self.conditions = {}

    def update_condition(self, op, key, value):
        """
        update condition with the given (op, key, value)
        """
        op_dict = {}
        op_dict[op] = value
        self.conditions[key] = op_dict

    def eq(self, key, value):
        self.update_condition(ConditionOp._EQ_, key, value)

    def ne(self, key, value):
        self.update_condition(ConditionOp._NE_, key, value)

    def gt(self, key, value):
        self.update_condition(ConditionOp._GT_, key, value)

    def ge(self, key, value):
        self.update_condition(ConditionOp._GE_, key, value)

    def lt(self, key, value):
        self.update_condition(ConditionOp._LT_, key, value)

    def le(self, key, value):
        self.update_condition(ConditionOp._LE_, key, value)

    def limit(self, offset, count):
        if offset < 0:
            offset = 0
        if count < 0:
            count = 0
        op_dict = {}
        op_dict[ConditionOp._LIMIT_] = str(offset) + "," + str(count)
        self.conditions["limit"] = op_dict

    def get_conditions(self):
        return self.conditions

    def set_conditions(self, conditions):
        self.conditions = conditions
