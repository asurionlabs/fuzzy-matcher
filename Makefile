###
# Fuzzy Matcher is an AWS Lambda interface to perform fuzzy matching.
# Fuzzy matching is useful for comparing if string are similar but not necessarily
# exact, such as the spelling of a person's name compared to the name in a contact 
# database.
# 
# Copyright (C) 2018-2019  Asurion, LLC
#
# Fuzzy Matcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fuzzy Matcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fuzzy Matcher.  If not, see <https://www.gnu.org/licenses/>.
###

PYVERSION ?= 3.6
APP_NAME = fuzzy-matcher

.PHONY: build
build:
	@python3 --version 2>&1 | grep $(PYVERSION)
	@if [ -d "dist" ]; then rm -rf dist/; fi
	@if [ -d "target" ]; then rm -rf target/; fi
	@mkdir dist target
	@cp -r *.py requirements.txt dist/
	@pip3 install -r requirements.txt -t dist
	@pip3 install nltk
	@python3 -m nltk.downloader -d dist/nltk_data punkt
	@echo "Cleaning up unnecessary files"
	@rm -rf dist/nltk_data/tokenizers/*.zip
	@rm -rf dist/nltk_data/tokenizers/punkt/*.pickle
	@echo Copying sqlite3 binary that is normally included in python3, but Amazon Lambda AMI is missing
	@echo This is required for nltk to function on lambda
	@cp /usr/lib64/python3.6/lib-dynload/_sqlite3.cpython-36m-x86_64-linux-gnu.so dist/
	@echo "building zip package"
	@find dist/ -type f -name "*.py[co]" -exec rm {} +
	@cd dist && zip -r $(APP_NAME).zip *
	@cd ..
	@mv dist/$(APP_NAME).zip target/$(APP_NAME).zip
	@rm -rf dist/
	@echo "Deployment package is ready at target/$(APP_NAME).zip"