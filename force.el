;;; force.el -- food ordering system
;;; Commentary:
;;; Code:

(setq force-project-name "force"
      force-project-dir "~/Documents/Stuff/force/"
      force-elconf-buffer (project-buffer-name-by-feature
                           force-project-name
                           "emacs-config")
      force-org-buffer (project-buffer-name-by-feature
                        force-project-name
                        "organizer")
      force-shell-buffer (project-buffer-name-by-feature
                          force-project-name
                          "main-shell")
      force-prodigy-buffer (project-buffer-name-by-feature
                            "prodigy"
                            force-project-name))

(defun buffer-exists (bufname)
  (not (eq nil (get-buffer bufname))))

(prodigy-define-service
  :name "Force"
  :command "~/.virtualenvs/force/bin/python"
  :args '("manage.py" "runserver")
  :init (lambda ()
          (prodigy-define-service
            :name "Force: Webpack Observer"
            :command "node"
            :args '("./node_modules/webpack/bin/webpack.js" "--watch")
            :cwd (concat force-project-dir)
            :stop-signal 'kill
            :kill-signal 'sigkill
            :kill-process-buffer-on-stop t)

          (defun force-menu-cleanup ()
            (interactive)
            (bpr-spawn "force cleanup"))

          (defun force-menu-fetch ()
            (interactive)
            (bpr-spawn "force fetch"))

          (defun force-push (cm)
            (interactive "MCommit message: ")
            (let* ((bpr-process-directory force-project-dir))
              (bpr-spawn (concatenate 'string "fab push:cm=\'" cm "\'"))))

          (defun force-deploy ()
            (interactive)
            (let* ((bpr-process-directory force-project-dir))
              (bpr-spawn "fab deploy")))

          (venv-workon force-project-name)
          (spawn-shell force-shell-buffer force-project-dir)
          (with-current-buffer (find-file-noselect (concatenate 'string force-project-dir "/" force-project-name ".el"))
            (rename-buffer force-elconf-buffer))
          (with-current-buffer (find-file-noselect (concatenate 'string force-project-dir "/" force-project-name ".org"))
            (rename-buffer force-org-buffer)))
  :cwd force-project-dir
  :url "http://localhost:8000/"
  :tags '(django react node)
  :stop-signal 'kill
  :kill-signal 'sigkill
  :port 8000
  :env '(("DATABASE_URL" "postgres://akatovda:qwadzv@localhost:5432/force")
         ("DEBUG" "1"))
  :kill-process-buffer-on-stop t)
(provide 'force)
;;; force.el ends here
