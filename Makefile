_today =`date '+%Y-%m-%d  %H:%M:%S'`
_commit_name = "autocommit $(_today)"
app_name = weather_bot
_path = $(CURDIR)

_service-path = ~/.config/systemd/user

push:
	@$(MAKE) --no-print-directory _black
	@$(MAKE) --no-print-directory _git_commit
	@echo "\n⚙️  pushing as $(_commit_name)\n"
	@git push origin main
	@echo "\n✅  done!"

push-force:
	@$(MAKE) --no-print-directory _black
	@$(MAKE) --no-print-directory _git_commit
	@echo "\n⚙️  🚩FORCE🚩  pushing as $(_commit_name)\n"
	@git push --force origin main
	@echo "\n✅  done!"

_black:
	@cd $(_path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .

_git_commit:
	@cd $(_path)
	@echo "\n⚙️  making commit $(app_name)...\n"
	@git add .
	-@git commit -m $(_commit_name)

_stop-service:
	-@systemctl --user stop $(app_name)
	@echo "\n❌  service stopped\n"


_start-service:
	@systemctl --user restart $(app_name)
	@echo "\n✅  service started\n"

setup:
	@cd $(_path)
	@echo "\n📝  installing dependencies...\n"
	@pip3.10 install -r ./misc/requirements.txt
	@sudo apt-get install python3-systemd

	@$(MAKE) --no-print-directory copy-service

	@echo "\n✅ setup complete!"

start-python:
	python3.10 app.py

status:
	-@systemctl --user status $(app_name) | cat

stop:
	@$(MAKE) --no-print-directory _stop-service

start:
	@$(MAKE) --no-print-directory _start-service
	@sleep 2
	@$(MAKE) --no-print-directory status

copy-service:
	@echo "\n⚙️  moving service to $(_service-path)\n"
	@sudo cp $(_path)/service/$(app_name).service $(_service-path)/$(app_name).service
	@echo "\n⚙️  managing service \n"
	-@systemctl --user daemon-reload
	-@systemctl --user enable $(app_name)
	@echo "\n✅  done!"

cat-service:
	@systemctl --user cat $(app_name)

cat-log:
	@journalctl --user --unit=$(app_name)