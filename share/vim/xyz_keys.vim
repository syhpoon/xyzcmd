setlocal iskeyword+=!

syn case match

"""load :ns:plugin
syn match xyzComment /#.*/
syn match xyzLoad /load/ nextgroup=xyzNSPath skipwhite
syn match xyzNSPath /\(\:[^ ]\+\)/ contained skipwhite

"""from :ns:plugin load method
syn match xyzFromLoad /from/ nextgroup=xyzFromNSPath contains=xyzFromNSPath skipwhite
syn match xyzFromNSPath /\(\:[^ ]\+\)/ nextgroup=xyzLoadPlugin contained skipwhite
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
