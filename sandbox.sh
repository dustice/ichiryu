#!/bin/bash
ulimit -t 3 -m 300000
luajit sandbox.lua lua_in.lua 1> >(head -c2000) 2> >(head -c2000 1>&2)
