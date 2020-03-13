inoremap <silent><expr> <c-space> coc#refresh()

call coc#config('coc.preferences', {
			\ "autoTrigger": "always",
			\ "maxCompleteItemCount": 10,
			\ "codeLens.enable": 1,
			\ "diagnostic.virtualText": 1,
			\ "languageserver": {
      \ "golang": {
      \  "command": "gopls",
      \  "rootPatterns": ["go.mod", ".vim/", ".git/", ".hg/"],
      \  "filetypes": ["go"],
      \  "initializationOptions": {
      \     "usePlaceholders": 1,
      \     },
      \   },
      \ },
      \})

let s:coc_extensions = [
			\ 'coc-dictionary',
			\ 'coc-json',
			\ 'coc-ultisnips',
			\ 'coc-tag',
			\]

for extension in s:coc_extensions
	call coc#add_extension(extension)
endfor
