(defun force ()
  "initialize force development workflow"
  (interactive)
  (defvar *-project-name "force")
  (defvar force-server t)
  (defvar force-root-dir "/Volumes/Main/Users/akatovda/Documents/Stuff/force")
  (setenv "DATABASE_URL" "postgres://akatovda:qwadzv@localhost:5432/force")
  (venv-workon *-project-name)
  (dz-defservice force-server "python"
                 :args ("manage.py" "runserver")
                 :cd force-root-dir)
  (elscreen-create)
  (force-server-start)
  (delete-other-windows)
  (spawn-shell "*force-shell*" force-root-dir)
  (delete-other-windows))

(provide 'force)
