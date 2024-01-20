#include <iostream>
#include <string>
#include <stdio.h>

int main(){

    /* -------------------- */
    /* VARIABLE DECLARATION */
    /* -------------------- */
   
    /* variable initilization in C++ can take many forms but the one
       with curly braces are favored. It is also important to note that
       it is good practice to always initialize our variables upon creation */

    /* for instance, we can declare variables just like in C */
    int age = 28;

    /* but for best practices, a better way to initilize a variable 
       is with curly braces */
    int year {1995};

    /* to declare multiple variables, we simply do this */
    int month {7}, day {19};

    printf("I am %d years old and was born on the %dth of the month %d of the year %d \n", 
           age, day, month, year);

   /* ------------------ */
   /* GETTING USER INPUT */
   /* ------------------ */

   /* a way to get user input in C++ is to use cin input */
   std::string name;
   std::cout << "What's your name? \n";
   std::cin >> name;
   printf("Hello %s \n", name.c_str());

   /* for naming variabels and functions, either camelCase or underscore
      naming can be used */

      /* int my_variable;
         double myVariable; */

      /* multiple line strings */
   std::cout << "This is an example of"
                " a multi line string";

      /* keep lines 80 characters long or less */

      /* use whitespaces to make code easier to read */
      /* int cost         = 57;
         int pricePerItem = 24; */

    return 0;
}

