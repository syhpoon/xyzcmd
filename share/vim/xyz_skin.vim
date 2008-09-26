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
" skin file syntax
"

runtime! syntax/xyz_block.vim

syn match xyz_skinRuleset /fs\.rules/
syn match xyz_skinRuleset /ui\.\S\+/

syn keyword xyz_skinColor BLACK BROWN YELLOW WHITE DEFAULT DARK_BLUE
syn keyword xyz_skinColor DARK_RED DARK_GREEN DARK_GRAY LIGHT_GRAY LIGHT_RED
syn keyword xyz_skinColor LIGHT_BLUE LIGHT_MAGENTA LIGHT_CYAN BOLD UNDERLINE
syn keyword xyz_skinColor STANDOUT DARK_MAGENTA DARK_CYAN LIGHT_GREEN

syn match xyz_skinMetavar /^\s*AUTHOR/ 
syn match xyz_skinMetavar /^\s*VERSION/ 
syn match xyz_skinMetavar /^\s*DESCRIPTION/ 

highlight link xyz_skinColor Keyword
highlight link xyz_skinMetavar Identifier
highlight link xyz_skinRuleset Keyword
