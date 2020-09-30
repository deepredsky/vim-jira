if !has('python3')
  echo 'vim-jira requires Vim compiled with +python3!'
  finish
endif

if !exists("g:jira_url")
  let g:jira_url = 'https://jira.atlassian.com'
endif

execute 'python3 import sys'
execute "python3 sys.path.append(r'" . expand("<sfile>:p:h")  . "')"
execute "python3 from vimjira import vim_jira, vim_jira_link"

command! -nargs=? Jira python3 vim_jira(<f-args>)

au! BufRead,BufNewFile *.jira set filetype=jira
