# vim-jira

Browse JIRA inside Vim!

Basically a clone of [vim-reddit](https://github.com/joshhartigan/vim-reddit)
with some ux tweaks from [gv.vim](https://github.com/junegunn/gv.vim)

![vim jira screenshot](https://raw.githubusercontent.com/deepredsky/vim-jira/master/vim-jira-screenshot.png)

## Installation

This plugin requires python3

Using [vim-plug]( https://github.com/junegunn/vim-plug )

```vim
    Plug 'deepredsky/vim-jira'
```

## Configuration

You can configure the following settings which is required to make this plugin work

Set this to board_id and the base url of the jira installation.

```vim
    let g:jira_url = 'https://acme.atlassian.net'
    let g:jira_board_id = 31
```

Configure username and secret to access your jira installation. Api token can
be generated at https://id.atlassian.com/manage/api-tokens

```vim
    export JIRA_USERNAME=your.jira.email@acme.com
    export JIRA_API_TOKEN=super-secret-token
```

## Usage

Open issues browser for the current sprint for your jira board

```vim
  :JiraSprint
```
These mappings are available in the jira browser

- `o` or `<cr>` on a issue to display the content of it
- `]]` and `[[` to move between issues
- <ctrl-n> <ctrl-p> to go to next/prev issue
- `q` to close

Single issue can be opened with `Jira` command. it accepts both the issue id
and key

```vim
:Jira FOO-1
:Jira 1234
```

Without arguments `Jira' will open current list of 50 issues in your project

## License

This plugin is MIT licensed.
See https://github.com/deepredsky/vim-jira/blob/master/LICENSE

## Bugs

If you find a bug please post it on the issue tracker:
http://github.com/deepredsky/vim-jira/issues/

## Contributing

Think you can make this plugin better?  Awesome!  Fork it on GitHub and send a
pull request.

GitHub: http://github.com/deepredsky/vim-jira

## Credits

* [Josh](https://github.com/joshhartigan) for [vim-reddit](https://github.com/joshhartigan/vim-reddit)
* [ryanss](https://github.com/ryanss) for [vim-hackernews](https://github.com/ryanss/vim-hackernews)
* [junegunn](https://github.com/junegunn) for [gv.vim](https://github.com/junegunn/gv.vim)
