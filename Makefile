_today =`date '+%Y-%m-%d_%H:%M:%S'`
_commit_name = "autocommit_$(_today)"
app_name = weather_bot
_path = $(CURDIR)

_service-path = ~/.config/systemd/user
_common-service-path = /etc/systemd/system/

push:
	@$(MAKE) --no-print-directory _black
	@$(MAKE) --no-print-directory _git_commit
	@echo "\n⚙️  pushing as $(_commit_name)\n"
	@git push origin main
	@$(MAKE) --no-print-directory _echo_done

push-force:
	@$(MAKE) --no-print-directory _black
	@$(MAKE) --no-print-directory _git_commit
	@echo "\n⚙️  🚩FORCE🚩  pushing as $(_commit_name)\n"
	@git push --force origin main
	@$(MAKE) --no-print-directory _echo_done

_black:
	@cd $(_path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .

_git_commit:
	@cd $(_path)
	@echo "\n⚙️  making commit $(_commit_name)...\n"
	@git add .
	-@git commit -m $(_commit_name)

_stop-service:
	-@systemctl --user stop $(app_name)
	@echo "\n❌  service stopped\n"

_stop-common-service:
	-@sudo systemctl stop $(app_name)_common
	@echo "\n❌  common service stopped\n"

_start-service:
	@systemctl --user restart $(app_name)
	@echo "\n✅  service started\n"

_start-common-service:
	@sudo systemctl restart $(app_name)_common
	@echo "\n✅  common service started\n"

_echo_done:
	@echo "\n✅  done!\n"

setup:
	@cd $(_path)
	@echo "\n📝  installing dependencies...\n"
	@wget -qO - https://raw.githubusercontent.com/tvdsluijs/sh-python-installer/main/python.sh | sudo bash -s 3.10.0

	@pip3.10 install -r ./misc/requirements.txt
	@sudo apt-get install python3-systemd
	@sudo apt-get install python3-dev python3-rpi.gpio
	@sudo apt-get install i2c-tools
	@sudo apt-get install git

	@$(MAKE) --no-print-directory copy-service

	@echo "\n✅ setup complete!\n"

	@$(MAKE) --no-print-directory start

start-python:
	@python3.10 app.py

status:
	-@systemctl --user status $(app_name) | cat

status-common:
	-@sudo systemctl status $(app_name)_common | cat

stop:
	@$(MAKE) --no-print-directory _stop-service

stop-common:
	@$(MAKE) --no-print-directory _stop-common-service

start:
	@$(MAKE) --no-print-directory _start-service

start-common:
	@$(MAKE) --no-print-directory _start-common-service

copy-service:
	@echo "\n⚙️  moving service to $(_service-path)\n"
	@mkdir -p $(_service-path)
	@sudo cp $(_path)/service/$(app_name).service $(_service-path)/$(app_name).service
	@echo "\n⚙️  managing service \n"
	-@systemctl --user daemon-reload
	-@systemctl --user enable $(app_name)
	@$(MAKE) --no-print-directory _echo_done


copy-common-service:
	@echo "\n⚙️  moving service to $(_common-service-path)\n"
	@# @mkdir -p $(_common-service-path)
	@sudo cp $(_path)/service/$(app_name)_common.service $(_common-service-path)/$(app_name)_common.service
	@echo "\n⚙️  managing service \n"
	-@sudo systemctl daemon-reload
	-@sudo systemctl enable $(app_name)_common
	@$(MAKE) --no-print-directory _echo_done




cat-service:
	@systemctl --user cat $(app_name)

cat-log:
	@journalctl --user --unit=$(app_name)