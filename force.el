(defun force ()
  "initialize force development workflow"
  (interactive)
  (defvar force-server t)
  (dz-defservice force-server "python"
                 :args ("app.py")
                 :cd "/Volumes/Main/Users/akatovda/Documents/Stuff/force")
  (elscreen-create)
  (force-server-start)
  (delete-other-windows)
  (spawn-shell "*force-shell*" "/Volumes/Main/Users/akatovda/Documents/Stuff/force/")
  (delete-other-windows))

(provide 'force)
