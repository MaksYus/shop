#!/bin/bash
set -a
source .env
set +a

alembic upgrade head