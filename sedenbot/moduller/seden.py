# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from sedenbot import KOMUT, CHANNEL
from sedenecem.core import edit, reply, extract_args, sedenify

@sedenify(pattern='^.dto')
def dto(message):
    dto = extract_args(message).lower()
    if seden:
        if dto in KOMUT:
            edit(message, str(KOMUT[dto]))
        else:
            edit(message, '**Xahiş edirik bir bot modulu yazın.**')
    else:
        edit(message, '**Xahiş edirik hansı bot modulu üçün məlumat almaq istədiyinizi yazın !\
            \nKullanım:** `.dto <modül adı>`')
        metin = f'**[Dto UserBot](https://t.me/{CHANNEL}) Yüklü Modullər:**\n'
        for liste in KOMUT:
            metin += '- `' + str(liste)
            metin += '` \n'
        reply(message, metin, preview=False)
