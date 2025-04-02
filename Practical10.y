%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void yyerror(const char *s);
int yylex();
%}

%union 
{
    int fval;
}

%token <fval> NUMBER
%token '+' '-' '*' '/' '^' '(' ')'

%type <fval> E T F G L

%left '+' '-'
%left '*' '/'
%right '^'
%left '(' ')'

%%

L   : E  {printf("=%d\n",$$); return 0;}
     ;
E   : E '+' T   { $$ = $1 + $3; }
    | E '-' T   { $$ = $1 - $3; }
    | T         { $$ = $1; }
    ;

T   : T '*' F   { $$ = $1 * $3; }
    | T '/' F   { $$ = $1 / $3; }
    | F         { $$ = $1; }
    ;

F   : G '^' F   { $$ = pow($1, $3); } 
    | G         { $$ = $1; }
    ;

G   : '(' E ')' { $$ = $2; }
    | NUMBER    { $$ = $1; }
    ;


%%

void yyerror(const char *s) {
    printf("Error: %s\n", s);
}

int main() {
    printf("Enter an arithmetic expression: ");
    yyparse();
    return 0;
}
