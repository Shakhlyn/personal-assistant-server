#!/usr/bin/env bash

set -e

log() {
    printf '[+] %s\n' "$1"
}

create_dirs() {
    log "Creating directories"

    mkdir -p \
        app/{api,core,schemas,models,services,repositories,db,utils} \
        scripts \
        tests

    printf '    app/{api,core,schemas,models,services,repositories,db,utils}\n'
    printf '    scripts\n'
    printf '    tests\n'
    printf '    \n'
}

create_files() {
    log "Creating files"

    local files=(
        app/__init__.py
        app/api/__init__.py
        app/core/__init__.py
        app/core/config.py
        app/core/exceptions.py
        app/core/logging.py
        app/core/middleware.py
        app/core/request_id.py
        app/core/security.py
        app/schemas/__init__.py
        app/models/__init__.py
        app/services/__init__.py
        app/repositories/__init__.py
        app/db/__init__.py
        app/db/base.py
        app/db/session.py
        app/utils/__init__.py
        tests/__init__.py
    )

    for file in "${files[@]}"; do
        touch "$file"
        printf '    %s\n' "$file"
    done

    printf '    \n'
}


create_dirs
create_files

log "Monolith project structure created successfully"
