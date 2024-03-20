; This project, and all source code, is licensed under the BSD 3-Clause license.
; This should be found at the root of this project's directory.
; If you cannot find it, you can find a copy here: https://github.com/1Codealot/Bismuth/blob/master/LICENSE

section .text
exit:
    mov rax, 60
    mov rdi, [ rsp + 8 ] ;; exit_code
    syscall
    ret