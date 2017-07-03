/* rand example: guess the number */
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
using namespace std;



int main ( int argc , char ** argv ) {
 
   if ( argc != 2 ) {
     cout << "error (no input file)" << endl;
     return 1;
   }

   srand (ftime()*1000/2250);
   int f = rand(); 

   cout << f;	
   cout << endl;
 
   return 0;
 }
 
