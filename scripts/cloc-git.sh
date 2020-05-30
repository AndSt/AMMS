#!/usr/bin/env bash
git clone --depth 1 "git@github.com:AndSt/AMMS.git" temp-linecount-repo &&
  printf "('temp-linecount-repo' will be deleted automatically)\n\n\n" &&
  cloc temp-linecount-repo &&
  rm -rf temp-linecount-repo
