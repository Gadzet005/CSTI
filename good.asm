extern io_get_dec 
extern io_print_dec 
extern io_newline 

section.text: 
global main 
main: 
    call io_get_dec
    cdq
    xor eax, edx
    sub eax, edx
    call io_print_dec
    call io_newline
    
    
    xor eax, eax 
    ret
