;; theming
(add-to-list 'custom-theme-load-path ;; location of themes
   "~/.emacs.d/themes/busybee")
(load-theme 'busybee t) ;; select busybee theme
(menu-bar-mode -1)      ;; disable menu bar

;; flyspell
(flyspell-mode 1) ;; enable spell-checking

;; elpa
(require 'package)
(add-to-list 'package-archives ;; augment packages with MELPA repository
  '("melpa" . "http://melpa.milkbox.net/packages/") t)
(package-initialize)
;; ido
(ido-mode t)       ;; enable ido
(ido-ubiquitous t) ;; for all of the things


;; automatically configured shizzle
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-safe-themes (quote ("9562e9eb5fd01677ac6b76b66f9a81338991fa9d270270802eeae5232c8da0a6" default))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
