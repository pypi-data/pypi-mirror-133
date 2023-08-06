#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._base import TranscribeInterpreter


class ASCIIRenderer(TranscribeInterpreter):
    '''Creates ASCII representations for tensor expressions.'''

    _traversal_order = TranscribeInterpreter.TraversalOrder.POST

    as_payload = TranscribeInterpreter.as_payload('ascii')

    @as_payload
    def literal(self, value, **kwargs):
        return str(value)

    @as_payload
    def tensor(self, abstract, **kwargs):
        return str(abstract.symbol)

    @as_payload
    def index(self, item, bound, kron, **kwargs):
        if bound:
            return f'~{str(item.symbol)}'
        elif kron:
            return f'*{str(item.symbol)}'
        else:
            return str(item.symbol)

    @as_payload
    def indices(self, items, **kwargs):
        return ','.join([i.ascii for i in items])

    @as_payload
    def index_notation(self, indexless, indices, **kwargs):
        return f'[{indices.ascii}]'

    @as_payload
    def call(self, f, x, **kwargs):
        return f

    @as_payload
    def neg(self, x, **kwargs):
        return ''

    @as_payload
    def matmul(self, lhs, rhs, **kwargs):
        return ''

    @as_payload
    def kron(self, lhs, rhs, **kwargs):
        return ''

    @as_payload
    def binary(self, lhs, rhs, precedence, oper, **kwargs):
        return f'{oper}'

    @as_payload
    def ein(self, lhs, rhs, precedence, reduction, pairwise, outidx, **kwargs):
        suffix = f' -> {outidx.ascii}' if outidx is not None else ''
        return f'{reduction}:{pairwise}' + suffix

    @as_payload
    def tran(self, src, indices, **kwargs):
        return f'-> [{indices.ascii}]'
