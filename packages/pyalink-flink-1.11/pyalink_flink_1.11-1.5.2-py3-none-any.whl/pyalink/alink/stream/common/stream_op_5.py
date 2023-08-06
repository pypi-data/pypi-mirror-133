#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import StreamOperator, BaseSinkStreamOp, BaseModelStreamOp


class VectorToTensorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.VectorToTensorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToTensorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTensorDataType(self, val):
        return self._add_param('tensorDataType', val)

    def setTensorShape(self, val):
        return self._add_param('tensorShape', val)


class VectorToTripleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.VectorToTripleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToTripleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColumnValueSchemaStr(self, val):
        return self._add_param('tripleColumnValueSchemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class WhereStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.WhereStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WhereStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)


class WindowGroupByStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.WindowGroupByStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WindowGroupByStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setSessionGap(self, val):
        return self._add_param('sessionGap', val)

    def setSlidingLength(self, val):
        return self._add_param('slidingLength', val)

    def setWindowLength(self, val):
        return self._add_param('windowLength', val)

    def setGroupByClause(self, val):
        return self._add_param('groupByClause', val)

    def setIntervalUnit(self, val):
        return self._add_param('intervalUnit', val)

    def setWindowType(self, val):
        return self._add_param('windowType', val)


class Word2VecPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.Word2VecPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2VecPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPredMethod(self, val):
        return self._add_param('predMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)


class WriteTensorToImageStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.image.WriteTensorToImageStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WriteTensorToImageStreamOp, self).__init__(*args, **kwargs)
        pass

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setImageType(self, val):
        return self._add_param('imageType', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

