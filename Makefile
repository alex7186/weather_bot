_today =`date '+%Y-%m-%d_%H:%M:%S'`
_commit_name = "autocommit_$(_today)"
app_name = weather_bot
_path = $(CURDIR)

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
	@echo "\n⚙️  making commit with name $(_commit_name)...\n"
	@git add .
	-@git commit -m $(_commit_name)

_echo_done:
	@echo "\n✅  done!\n"

setup:
	@cd $(_path)
	@echo "\n📝  installing dependencies...\n"
	@wget -qO - https://raw.githubusercontent.com/tvdsluijs/sh-python-installer/main/python.sh | sudo bash -s 3.10.0

	@pip3.10 install -r ./misc/python_requirements.txt
	@sudo apt-get install $(cat ./misc/packages_requirements.txt)

	@$(MAKE) --no-print-directory copy-service
	@echo "\n✅ setup complete!\n"
	@$(MAKE) --no-print-directory start

start-python:
	@python3.10 app.py

status:
	-@sudo systemctl status $(app_name) | cat

stop:
	-@sudo systemctl stop $(app_name)
	@echo "\n❌  service stopped"

start:
	@sudo systemctl restart $(app_name)
	@echo "\n✅  service (re)started"

copy-service:
	@echo "\n⚙️  moving service to $(_common-service-path)\n"
	@# @mkdir -p $(_common-service-path)
	@sudo cp $(_path)/service/$(app_name).service $(_common-service-path)/$(app_name).service
	@echo "\n⚙️  managing service \n"
	-@sudo systemctl daemon-reload
	-@sudo systemctl enable $(app_name)
	@$(MAKE) --no-print-directory _echo_done

cat-log:
	@journalctl --unit=$(app_name)