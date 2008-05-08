"
" Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
"
" This file is part of XYZCommander.
" XYZCommander is free software: you can redistribute it and/or modify
" it under the terms of the GNU Lesser Public License as published by
" the Free Software Foundation, either version 3 of the License, or
" (at your option) any later version.
" XYZCommander is distributed in the hope that it will be useful,
" but WITHOUT ANY WARRANTY; without even the implied warranty of
" MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
" GNU Lesser Public License for more details.
" You should have received a copy of the GNU Lesser Public License
" along with XYZCommander. If not, see <http://www.gnu.org/licenses/>.

"
" conf/keys syntax file
"

setlocal iskeyword+=!

syn case match

"""load :ns:plugin
syn match xyzComment /#.*/
syn match xyzLoad /load/ nextgroup=xyzNSPath skipwhite
syn match xyzNSPath /\(\:[^ ]\+\)/ contained skipwhite

"""from :ns:plugin load method
syn match xyzFromLoad /from/ nextgroup=xyzFromNSPath contains=xyzFromNSPath skipwhite
syn match xyzFromNSPath /\(\:\S\+\)/ nextgroup=xyzLoadPlugin contained skipwhite
syn match xyzLoadPlugin /load/ nextgroup=xyzPlugin contained skipwhite
syn match xyzPlugin /\S\+/ contained

syn match xyzStatement /set chain key/

highlight link xyzLoad Statement
highlight link xyzFromLoad Statement
highlight link xyzLoadPlugin Statement
highlight link xyzStatement Statement
highlight link xyzComment Comment
highlight link xyzNSPath Identifier
highlight link xyzFromNSPath Identifier
highlight link xyzPlugin Identifier

"bind :misc:hello:say_hello to CTRL-R
"bind :misc:hello:say_hello to CTRL-R context DEFAULT
"bind! say_hello to CTRL-X

"set chain key META-Q
"set chain key META-L context XXX
