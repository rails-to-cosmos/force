;;; force.el -- food ordering system
;;; Commentary:
;;; Code:
(setq project-name "force"
      project-dir "~/Documents/Stuff/force/"
      venv-name "force"
      el-config-buffer (project-buffer-name-by-feature
                        project-name
                        "el-config")
      organizer-buffer (project-buffer-name-by-feature
                        project-name
                        "organizer")
      shell-buffer (project-buffer-name-by-feature
                    project-name
                    "shell")
      prodigy-buffer (project-buffer-name-by-feature
                      "prodigy"
                      project-name))

(prodigy-define-service
  :name "Force"
  :command "~/.virtualenvs/force/bin/python"
  :args '("manage.py" "runserver")
  :init (lambda ()
          (defun force-menu-cleanup ()
            (interactive)
            (bpr-spawn "force cleanup"))
          (defun force-menu-fetch ()
            (interactive)
            (bpr-spawn "force fetch"))
          (defun force-collectstatic ()
            (interactive)
            (let* ((bpr-process-directory project-dir))
              (bpr-spawn "force collectstatic --noinput")))
          (venv-workon venv-name)
          (spawn-shell shell-buffer project-dir)
          (find-file (concatenate 'string project-dir "/" project-name ".el"))
          (rename-buffer el-config-buffer)
          (find-file (concatenate 'string project-dir "/" project-name ".org"))
          (rename-buffer organizer-buffer)
          (switch-to-buffer prodigy-buffer)
          ;; (delete-other-windows)
          ;; (split-window-horizontally)
          ;; (switch-to-buffer shell-buffer)
          )
  :cwd project-dir
  :url "http://localhost:8000/"
  :tags '(django)
  :stop-signal 'kill
  :kill-signal 'sigkill
  :port 8000
  ;; (spawn-shell (project-buffer-name-by-feature project-name "heroku") project-dir "heroku run bash --app sizo")
  :env '(("DATABASE_URL" "postgres://akatovda:qwadzv@localhost:5432/force"))
  :kill-process-buffer-on-stop t)
(provide 'force)
;;; force.el ends here
