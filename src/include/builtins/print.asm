section .text
print:
    mov rax, 1
    mov rdi, 1
    mov rsi, [ rsp + 8  ] ;; message
    mov rdx, [ rsp + 16 ] ;; message_len
    syscall
    ret