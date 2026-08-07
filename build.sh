#! /bin/bash
set -e

BUILD_CONTAINER_NAME="owul-builder"
VENV="venv"

show_help(){
    echo "usage: build.sh [-h|--help] [--venv]"
    echo ""
    echo "options:"
    echo "  -h, --help              show this message and exit"
    echo "  -venv                   install the project in 'editable mode' in the virtual environment"
    echo ""
}

build_build_container(){
    docker build -t "$BUILD_CONTAINER_NAME" -f Dockerfile.build .
}

build_repo(){
    docker run --rm -v "$(pwd)":/build $BUILD_CONTAINER_NAME make
}

build_app_container(){
    docker build -t "open-wake-up-light" .
}

ensure_venv_exists(){
    if test ! -d "$VENV"; then
        echo "Creating python virtual environment"
        python -m venv venv
        pip install --upgrade pip
    fi
}

install_in_venv(){
    pip install -e .
}


PROJECT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $PROJECT_DIR

venv_flag=false
while test "$#" -gt 0; do
    case "$1" in 
        --venv)
            venv_flag=true
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option '$1'"
            show_help
            exit 128
            ;;
    esac
    shift

done

if test "$venv_flag" = true; then
    ensure_venv_exists
    source "$VENV/bin/activate"
    install_in_venv
fi

build_build_container
build_repo
build_app_container

