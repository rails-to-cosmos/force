(defun force ()
  "initialize force development workflow"
  (interactive)
  (defun project-buffer-name-by-feature (project-name feature-name)
    (concatenate 'string "*" project-name "-" feature-name "*"))
  (defvar project-name "force")
  (defvar force-server t)
  (defvar force-root-dir "/Volumes/Main/Users/akatovda/Documents/Stuff/force")
  (setenv "DATABASE_URL" "postgres://akatovda:qwadzv@localhost:5432/force")
  (venv-workon project-name)

  (dz-defservice force-server "python"
                 :args ("manage.py" "runserver")
                 :cd force-root-dir)

  (elscreen-create)
  (force-server-start)
  (delete-other-windows)
  (spawn-shell (project-buffer-name-by-feature project-name "shell") force-root-dir)
  (spawn-shell (project-buffer-name-by-feature project-name "heroku") force-root-dir "heroku run bash --app sizo")

  (find-file (concatenate 'string force-root-dir "/" project-name ".el"))
  (rename-buffer (project-buffer-name-by-feature project-name "elisp"))

  (find-file (concatenate 'string force-root-dir "/" project-name ".org"))
  (rename-buffer (project-buffer-name-by-feature project-name "organizer"))

  (delete-other-windows))

(provide 'force)
