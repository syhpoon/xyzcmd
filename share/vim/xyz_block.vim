"
" Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
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
" block-structured configuration file syntax
"

syn match xyzComment /#.*/
syn match xyz_skinMacro /&\S\+/
syn match xyz_skinDigit /\d\+/
syn region xyz_skinString start=/"/ end=/"/ end=/$/ excludenl
syn region xyz_skinMultiString start=/'''/ end=/'''/

highlight link xyzComment Comment
highlight link xyz_skinString String
highlight link xyz_skinMultiString String
highlight link xyz_skinMacro Macro
highlight link xyz_skinDigit Number
