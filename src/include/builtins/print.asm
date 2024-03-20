; This project, and all source code, is licensed under the BSD 3-Clause license.
; This should be found at the root of this project's directory.
; If you cannot find it, you can find a copy here: https://github.com/1Codealot/Bismuth/blob/master/LICENSE

section .text
print:
    mov rax, 1
    mov rdi, 1
    mov rsi, [ rsp + 8  ] ;; message
    mov rdx, [ rsp + 16 ] ;; message_len
    syscall
    ret