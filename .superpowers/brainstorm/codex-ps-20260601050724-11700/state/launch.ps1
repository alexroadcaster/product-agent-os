$env:BRAINSTORM_DIR = 'C:\Users\user\Desktop\project\codex_docs\.superpowers\brainstorm\codex-ps-20260601050724-11700'
$env:BRAINSTORM_HOST = '127.0.0.1'
$env:BRAINSTORM_URL_HOST = '127.0.0.1'
$env:BRAINSTORM_PORT = '60621'
Remove-Item Env:\BRAINSTORM_OWNER_PID -ErrorAction SilentlyContinue
& node 'C:\Users\user\.codex\plugins\cache\openai-curated\superpowers\fef63ecf\skills\brainstorming\scripts\server.cjs' 1>> 'C:\Users\user\Desktop\project\codex_docs\.superpowers\brainstorm\codex-ps-20260601050724-11700\state\server.log' 2>> 'C:\Users\user\Desktop\project\codex_docs\.superpowers\brainstorm\codex-ps-20260601050724-11700\state\server.err.log'
