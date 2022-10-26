DOUBLE x [5]
INT i 
INT j 
DOUBLE swap 
INT pos 
	EVAL  -2.0 
	ASS  x[0]
	EVAL  -3.0 
	ASS  x[1]
	EVAL  3.0 
	ASS  x[2]
	EVAL  5.0 
	ASS  x[3]
	EVAL  2.5 
	ASS  x[4]
	EVAL  5 
	ASS  pos
L 1 :	EVAL  pos 0 >  		/* while (line  18 ) */
	GOTOF L 2
	EVAL  0 
	ASS  i
L 3 :	EVAL  i pos 1 -  <  		/* while (line  20 ) */
	GOTOF L 4
	EVAL  i 1 +  
	ASS  j
	EVAL  x[i] x[j] >  		/* if (line  22 ) */
	GOTOF L 5
	EVAL  x[j] 
	ASS  swap
	EVAL  x[i] 
	ASS  x[j]
	EVAL  swap 
	ASS  x[i]
L 5 :
	EVAL  i 1 +  
	ASS  i
	GOTO L 3
L 4 :	EVAL  pos 1 -  
	ASS  pos
	GOTO L 1
L 2 :	EVAL  pos 0 >  		/* if (line  34 ) */
	GOTOF L 6
	EVAL  3.4 
	ASS  x[0]
	GOTO L 7
L 7 :	EVAL  3.7 
	ASS  x[0]
L 6 :
	EVAL  0 
	ASS  i
L 8 :	EVAL  i 5 <  		/* while (line  42 ) */
	GOTOF L 9
	PRINT  x[i]
	EVAL  i 1 +  
	ASS  i
	GOTO L 8
L 9 :	END
