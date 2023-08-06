#!/usr/bin/env python
# -*- coding: utf-8 -*-
from funfact.lang.interpreter._evaluation import Evaluator


class ElementwiseEvaluator(Evaluator):
    def tensor(self, abstract, data, slices, **kwargs):
        return data[tuple(slices)]

    def kron(self, lhs, rhs, slices, **kwargs):
        raise NotImplementedError()
