#include <stdio.h>

int main(void) {
    int a[2][3] = {{10000, 2, 30000}, {4, 50000, 6}};

    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 3; j++)
            printf("a[%d][%d]: %p\n", i, j, (void *)&a[i][j]);
}

/*
結果:
a[0][0]: 0x16d1eee70
a[0][1]: 0x16d1eee74
a[0][2]: 0x16d1eee78
a[1][0]: 0x16d1eee7c
a[1][1]: 0x16d1eee80
a[1][2]: 0x16d1eee84
*/
