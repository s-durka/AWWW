*/

/*@ requires len > 0 && \valid_range(a,0,len-1);
  @ ensures 0 <= \result < len &&
  @   \forall integer i; 0 <= i < len ==> a[i] <= a[\result];
  @*/
int max(int *a, int len) {
  int x = 0;
  int y = len-1;
  /*@ loop invariant 0 <= x <= y < len &&
    @      \forall integer i;
    @         0 <= i < x || y < i < len ==>
    @         a[i] <= \max(a[x],a[y]);
    @ loop variant y - x;
    @*/
  while (x != y) {
    if (a[x] <= a[y]) x++;
    else y--;
  }
  return x;
}

/*
Local Variables:
compile-command: "make array_max.why3ml"
End:
*/
