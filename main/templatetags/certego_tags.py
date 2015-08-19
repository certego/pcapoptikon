#!/usr/bin/env python
#
# certego_tags.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
#
# Author:   Pietro Delsante <p.delsante@certego.net>
#           www.certego.net
#
import hexdump
from django.template.defaultfilters import register


@register.filter("b64decode_hexdump")
def b64decode_hexdump(value, default=""):
    if isinstance(value, unicode):
        return hexdump.hexdump(
            value.decode('base64'),
            result='return'
        )
    elif isinstance(value, str):
        return hexdump.hexdump(
            unicode(value).decode('base64'),
            result='return'
        )
    else:
        return default
