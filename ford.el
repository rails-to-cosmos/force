(setq ford-dir "/Users/akatovda/Documents/Stuff/Ford")

(dz-defservice ford "python"
               :args ("manage.py" "server")
               :cd ford-dir)

(provide 'ford)
