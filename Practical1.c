#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool String(const char *str)
{
    int len = strlen(str);
    int i = 0;

    while (i < len && str[i] == 'a')
    {
        i++;
    }
    if (i < len - 1 && str[i] == 'b' && str[i + 1] == 'b' && i + 2 == len)
    {
        return true;
    }
    return false;
}

int main()
{
    char input[100];

    printf("Enter a string: ");
    if (fgets(input, sizeof(input), stdin) != NULL)
    {
        size_t len = strlen(input);
        if (len > 0 && input[len - 1] == '\n')
        {
            input[len - 1] = '\0';
        }

        if (String(input))
        {
            printf("Valid String\n");
        }
        else
        {
            printf("Invalid String\n");
        }
    }
    return 0;
}




































