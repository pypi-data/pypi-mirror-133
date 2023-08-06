#!/bin/sh -e

PROJECT_ID=$(gcloud config list --format 'value(core.project)')
VERSION=${VERSION:=latest}
docker build -t gcr.io/${PROJECT_ID}/cbpa:${VERSION} .
