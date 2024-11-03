import py0dws as zd
import sys

[palette, env] = zd.initialize ()
import echo
echo.install (palette)
zd.start (palette, env)
