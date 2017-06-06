if !has('python')
  echo 'vim-jira requires Vim compiled with +python!'
  finish
endif

if !exists("g:jira_url")
  let g:jira_url = 'https://jira.atlassian.com'
endif

execute 'python import sys'
execute "python sys.path.append(r'" . expand("<sfile>:p:h")  . "')"
execute "python from vimjira import vim_jira, vim_jira_link"

command! -nargs=? Jira python vim_jira(<f-args>)

au! BufRead,BufNewFile *.jira set filetype=jira
