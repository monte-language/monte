;; monte.el -- support for editing Monte code -*- lexical-binding: t -*-

(defvar monte-mode-map
  (let ((map (make-sparse-keymap)))
    ;; (define-key map [remap forward-sentence] 'monte-forward-block)
    ;; (define-key map [remap backward-sentence] 'monte-backward-block)
    ;; (define-key map "\177" 'monde-dedent-line-backspace)
    ;; (define-key map (kbd "<backtab>") 'monte-dedent-line)
    map)
  "Keymap for monte-mode.")

(defun monte-get-previous-line-indent ()
  (save-excursion
    (forward-line -1)
    (current-indentation)))

(defun monte-indent-line ()
  (interactive)
  (message "%s %s %s" this-command last-command (- (current-indentation) 4))
  (let ((previous-indent (monte-get-previous-line-indent))
        (is-cycling (eq this-command last-command)))
    (if is-cycling
        (if (eq (current-indentation) 0)
            (indent-to (+ previous-indent 4))
          (let ((place (- (current-indentation) 4)))
            (beginning-of-line)
            (delete-horizontal-space)
            (indent-to place)))
      (indent-to (+ previous-indent 4)))))

(defvar monte-font-lock-keywords
  `(,(rx symbol-start
         (or "as" "bind" "break" "catch" "continue" "def" "else" "escape"
             "exit" "extends" "export" "finally" "fn" "for" "guards" "if"
             "implements" "in" "interface" "match" "meta" "method" "module"
             "object" "pass" "pragma" "return" "switch" "to" "try" "var"
             "via" "when" "while")
         symbol-end)
    (,(rx symbol-start "def" (1+ space) (group (1+ (or word ?_))) (0+ space) ?\()
     (1 font-lock-function-name-face))
    (,(rx symbol-start "object" (1+ space) (group (1+ (or word ?_))))
     (1 font-lock-function-name-face))
    (,(rx symbol-start (or "def" "var") (1+ space) (group (1+ (or word ?_))) (0+ space) ?: ?=)
     (1 font-lock-variable-name-face))
    ))

(defvar monte-mode-syntax-table
  (let ((table (make-syntax-table)))
    (mapc (lambda (c) (modify-syntax-entry c "." table)) "$%*+-./:;<=>?@^|")
    (modify-syntax-entry ?+ "." table)
    (modify-syntax-entry ?# "<" table)
    (modify-syntax-entry ?\n ">" table)
    (modify-syntax-entry ?' "\"" table)
    (modify-syntax-entry ?` "\"" table)
    (modify-syntax-entry ?\ "\\" table)
    table)
  "Monte syntax table.")

;;;###autoload
(define-derived-mode monte-mode prog-mode "Monte"
  "Major mode for editing Montefiles.

\\{monte-mode-map}"
  (set (make-local-variable 'indent-tabs-mode) nil)
  (set (make-local-variable 'comment-start) "# ")
  (set (make-local-variable 'comment-start-skip) "#+\\s-*")
  (set (make-local-variable 'font-lock-defaults) '(monte-font-lock-keywords nil nil nil nil))
  (set (make-local-variable 'indent-line-function) 'monte-indent-line)
  (setq-local electric-indent-inhibit t))
