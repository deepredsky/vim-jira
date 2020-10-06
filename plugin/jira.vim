if !has('python3')
  echo 'vim-jira requires Vim compiled with +python3!'
  finish
endif

if !exists("g:jira_url")
  let g:jira_url = 'https://jira.atlassian.com'
endif

execute 'python3 import sys'
execute "python3 sys.path.append(r'" . expand("<sfile>:p:h")  . "')"
execute "python3 from vimjira import vim_jira, vim_jira_link, vim_jira_sprint"

function! JiraSprint(sprintId)
  if exists("g:jira_board_id")
    python3 vim_jira_sprint(vim.eval('a:sprintId'))
    nnoremap <silent> <buffer> o :call <sid>open()<cr>
    nnoremap <silent> <buffer> O :call <sid>open_browser()<cr>
  else
    echohl ErrorMsg | echo "vim-jira error: g:jira_board_id is not set." | echohl None
    return
  endif
endfunction

function! s:open()
  let line = getline('.')
  call s:split()
  call s:scratch()
  nnoremap <silent> <buffer> q :close<cr>
  python3 vim_jira_link(vim.eval('line'))
  wincmd p
  nnoremap <silent> <buffer> q    :$wincmd w <bar> close<cr>
  echo
endfunction

function! s:open_browser()
  let line = getline('.')
  python3 vim_jira_link(vim.eval('line'), in_browser=True)
endfunction

function! s:split()
  if getwinvar(winnr('$'), 'jira_details')
    $wincmd w
    enew
  else
    vertical botright new
  endif
  let w:jira_details = 1
endfunction

function! s:scratch()
  setlocal buftype=nofile bufhidden=wipe noswapfile nomodeline
endfunction

command! -nargs=? Jira python3 vim_jira(<f-args>)
command! -nargs=? -complete=command JiraSprint call JiraSprint(<q-args>)

au! BufRead,BufNewFile *.jira set filetype=jira
