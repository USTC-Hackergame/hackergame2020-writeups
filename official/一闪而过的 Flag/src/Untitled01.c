#include <stdio.h>
#include <windows.h>

void usleep(__int64 usec) 
{ 
    HANDLE timer; 
    LARGE_INTEGER ft; 

    ft.QuadPart = -(10*usec); // Convert to 100 nanosecond interval, negative value indicates relative time

    timer = CreateWaitableTimer(NULL, TRUE, NULL); 
    SetWaitableTimer(timer, &ft, 0, NULL, NULL, 0); 
    WaitForSingleObject(timer, INFINITE); 
    CloseHandle(timer); 
}

int main()
{
 char flag[100];
 int n = 20;
 flag[n++] = 'f';
 flag[n++] = 'l';
 flag[n++] = 'a';
 flag[n++] = 'g';
 flag[n++] = '{';
 flag[n++] = 'A';
 flag[n++] = 'r';
 flag[n++] = 'e';
 flag[n++] = '_';
 flag[n++] = 'y';
 flag[n++] = 'o';
 flag[n++] = 'u';
 flag[n++] = '_';
 flag[n++] = 'e';
 flag[n++] = 'y';
 flag[n++] = 'e';
 flag[n++] = 's';
 flag[n++] = '1';
 flag[n++] = 'g';
 flag[n++] = 'h';
 flag[n++] = 't';
 flag[n++] = '_';
 flag[n++] = 'g';
 flag[n++] = '0';
 flag[n++] = '0';
 flag[n++] = 'D';
 flag[n++] = '?';
 flag[n++] = '_';
 flag[n++] = 'c';
 flag[n++] = 'a';
 flag[n++] = 'n';
 flag[n++] = '_';
 flag[n++] = 'y';
 flag[n++] = 'o';
 flag[n++] = 'u';
 flag[n++] = '_';
 flag[n++] = 'd';
 flag[n++] = 'I';
 flag[n++] = 's';
 flag[n++] = 't';
 flag[n++] = '1';
 flag[n++] = 'n';
 flag[n++] = 'g';
 flag[n++] = 'u';
 flag[n++] = 'i';
 flag[n++] = 's';
 flag[n++] = 'h';
 flag[n++] = '_';
 flag[n++] = '1';
 flag[n++] = 'i';
 flag[n++] = 'I';
 flag[n++] = '?';
 flag[n++] = '}';
 flag[n++] = '\0';

 printf("%s\n", flag + 20);
 usleep(500000);
 return 0;
}
