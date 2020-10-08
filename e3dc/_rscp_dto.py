import binascii
import copy
import json
import traceback
from enum import Enum
from typing import Optional, Union

from e3dc.rscp_tag import RSCPTag, RSCPTag2Type
from e3dc.rscp_type import RSCPType

"""
This is a data wrapper to send and receive data to the e3dc.
It consists of a tag, the type, the data and the size of the data.
"""

class RSCPDTO:
    def __init__(self, tag: RSCPTag, rscp_type: RSCPType = RSCPType.Nil, data: Union[list, float, str, None, bytes] = None,
                 size: Optional[int] = None):
        self.tag = tag
        self.type = rscp_type
        if rscp_type == RSCPType.Nil:
            res = RSCPTag2Type.__getattr__(tag.name)
            if res:
                self.type = res['type']
            else:
                if isinstance(data, list):
                    iscontainer = True
                    if len(data) > 0:
                        for l in data:
                            if not isinstance(l, RSCPTag) and not isinstance(l, RSCPDTO):
                                iscontainer = False

                    if iscontainer:
                        print('iscontainer', self.tag.name)
                        self.type = RSCPType.Container

                self.data = data

        if self.type == RSCPType.Container and not data:
            self.data = []
        else:
            self.data = data
        self.size = size
        self.current_pos = 0

    def __add__(self, other):
        if self.type == RSCPType.Container:
            if isinstance(self.data, list):
                basis = self
                if isinstance(other, RSCPDTO):
                    basis.data.append(other)
                    return basis
                elif isinstance(other, RSCPTag):
                    basis.data.append(RSCPDTO(tag=other))
                    return basis
                elif isinstance(other, list):
                    basis.data += other
                    return basis

        raise ArithmeticError

    def __copy__(self):
        return RSCPDTO(tag = self.tag, rscp_type=self.type, data=copy.copy(self.data), size=self.size)

    def __iter__(self):
        return self

    def __next__(self):
        if isinstance(self.data, list):
            while self.current_pos < len(self.data):
                ret = self.data[self.current_pos]
                self.current_pos += 1
                return ret
        elif self.current_pos == 0:
            self.current_pos += 1
            return self.data

        self.current_pos = 0
        raise StopIteration()


    def __getitem__(self, key):
        if isinstance(self.data, list):
            result = []
            for data in self.data:
                if data.name == key:
                    result.append(data)

            if len(result) == 1:
                data = result[0]
                if isinstance(data.data, list):
                    return data
                else:
                    return data
            elif len(result) > 1:
                return result
        else:
            if self.data:
                if self.data.tag == RSCPTag.LIST_TYPE:
                    return self.data[key]
                elif self.data.name == key:
                    return self.data

        return None

    def __cmp__(self, item):
        if isinstance(item, RSCPDTO):
            if self.name == item.name:
                return True

        return False

    def __len__(self):
        if isinstance(self.data, list):
            return len(self.data)
        else:
            return 1

    def __contains__(self, item):
        if isinstance(self.data, list):
            for data in self.data:
                if isinstance(item, str):
                    if data.name == item:
                        return True
                elif isinstance(item, RSCPTag):
                    if data.name == item.name:
                        return True
                elif isinstance(item, RSCPDTO):
                    if data == item:
                        return True
        else:
            if self.data:
                if self.data.tag == RSCPTag.LIST_TYPE:
                    return item in self.data
                elif self.data.name == item:
                    return True

        return False

    def set_data(self, value):
        if self.type == RSCPType.Container and isinstance(value, list):
            for k,l in enumerate(value):
                if isinstance(l, RSCPTag):
                    value[k] = RSCPDTO(l)
        elif self.type == RSCPType.Nil:
            if value is not None:
                raise AttributeError('Daten bei leerem Datentyp nicht erlaubt')

        self._data = value

    def get_data(self):
        return self._data

    def asDict(self, translate = False):
        if self.type == RSCPType.Container:
            obj = {}
            dat: RSCPDTO
            for dat in self.data:
                if isinstance(dat, RSCPDTO):
                    d: dict = dat.asDict()
                    if isinstance(obj, list):
                        obj = obj + [d]
                    elif len([k for k in d.keys() if k in obj.keys()]) > 0:
                        obj = [obj, d]
                    else:
                        obj = {**obj, **d}
        else:
            if not translate:
                obj = self.data
            else:
                obj = repr(self)

        return {self.name:obj}

    def __round__(self, n=None):
        if self.type != RSCPType.Error:
            return round(self.data, n)
        else:
            return 0.0

    def __int__(self):
        if self.type != RSCPType.Error:
            return int(self.data)
        else:
            return 0

    def __float__(self):
        if self.type != RSCPType.Error:
            return float(self.data)
        else:
            return 0.0

    def __str__(self):
        messages = []
        if self.type == RSCPType.Container:
            messages.append("rscp: \t tag: " + self.tag.name + "\t type: " + self.type.name)
            for dat in self.data:
                ret = str(dat)
                ret = ret.replace("\n","\n\t")
                messages.append(" |--> " + ret)
        else:
            try:
                attr = RSCPTag2Type.__getattr__(self.tag.name)
                if attr:
                    if not isinstance(attr['type'], RSCPType):
                        enum_value = attr['type'](self.data).name
                        messages.append(
                            "rscp: \t tag: " + self.tag.name + "\t type: " + self.type.name + "\t data: " + str(
                                self.data) + "\t enumtype: " + str(attr['type']) + "\t enumdata: " + str(
                                enum_value))
                        return "\n".join(messages)
            except:
                traceback.print_exc()
                pass
            if self.type == RSCPType.ByteArray:
                print(type(self.data))
                data = binascii.hexlify(self.data)
                messages.append("rscp: \t tag: " + self.tag.name + "\t type: " + self.type.name + "\t data: " + str(data))
            else:
                messages.append("rscp: \t tag: " + self.tag.name + "\t type: " + self.type.name + "\t data: " + str(self.data))

        return "\n".join(messages)

    def __repr__(self):
        if self.type == RSCPType.Container:
            return None
        else:
            try:
                attr = RSCPTag2Type.__getattr__(self.tag.name)
                if attr:
                    if not isinstance(attr['type'], RSCPType):
                        enum_value = attr['type'](self.data).name
                        return str(enum_value)
            except:
                traceback.print_exc()

            return str(self.data)

    def get_name(self):
        return self.tag.name

    name = property(get_name)
    data = property(get_data, set_data)
