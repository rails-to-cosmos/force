(setq force-dir "/Users/akatovda/Documents/Stuff/Force")

(dz-defservice force "python"
               :args ("manage.py" "server")
               :cd force-dir)

(provide 'force)
