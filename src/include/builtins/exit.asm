section .text
exit:
    mov rax, 60
    mov rdi, [ rsp + 8 ] ;; exit_code
    syscall
    ret