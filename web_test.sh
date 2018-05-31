# set ZEEGUU_WEB_CONFIG in your .bashrc if you don't want to go with the default
[ -z $ZEEGUU_WEB_CONFIG ] && export ZEEGUU_WEB_CONFIG=`pwd`/default_web.cfg 
python -m zeeguu_web
