#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Union, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class MessageUserReaction(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.MessageUserReaction`.

    Details:
        - Layer: ``136``
        - ID: ``0x932844fa``

    Parameters:
        user_id: ``int`` ``64-bit``
        reaction: ``str``
    """

    __slots__: List[str] = ["user_id", "reaction"]

    ID = 0x932844fa
    QUALNAME = "types.MessageUserReaction"

    def __init__(self, *, user_id: int, reaction: str) -> None:
        self.user_id = user_id  # long
        self.reaction = reaction  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageUserReaction":
        # No flags
        
        user_id = Long.read(b)
        
        reaction = String.read(b)
        
        return MessageUserReaction(user_id=user_id, reaction=reaction)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(String(self.reaction))
        
        return b.getvalue()