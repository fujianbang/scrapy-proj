PROJ_DIR=`pwd`
VENV=${PROJ_DIR}/.env
PROJ_NAME=engine

if [ ! -e ${VENV} ];then
    virtualenv --never-download --prompt "(${PROJ_NAME})" ${VENV} -p $(type -p python3)
fi

source ${VENV}/bin/activate 

export PROJ_NAME
export PROJ_DIR


PYTHONDONTWRITEBYTECODE=1
export PYTHONDONTWRITEBYTECODE

export PYTHONPATH=${PROJ_DIR}:${PROJ_DIR}/libs:${PROJ_DIR}/settings
