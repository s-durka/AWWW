/* 
	zakładamy, że n = 2k
	tablica ma k zer i k jedynek
	chcemy posortować ją stabilnie i w miejscu
	(czyli do postaci [000...1111...])
*/

// dziel i zwyciężaj:

void mirror_image(int i, int j, int a[]) {
	while (i<j) {
		int tmp = a[i];
		a[i] = a[j];
		a[j] = tmp;
		i++;
		j--;
	}
}

void cyclic_rotation(int k, int i, int j, int & a[]) {
	// stabilnie i w miejscu obraca tablicę a[i...j] o k el. w lewo
	mirror_image(i, j, a);
	mirror_image(i, n - k - 1);
	mirror_image(n-k, j);

}

int lower_bound(int num, int l, int p, int a[]) {
	for (int j = r; j > l && a[j] == num; i++); // j - pierwszy od prawej o wartości num
		cyclic_rotation(m-i, i, j, a);
} 

void sort(int l, int r, int & a[]) {
	if (l < p) {
		int m = (l+r)/2;
		sort(l, m, a);
		sort(m+1, r, a);
		for (int i = l; i < m && a[i] == 0; i++); // i - indeks pierwszego elementu o wartości 1
		
	}
}

void ones_and_zeros(int & a[], int n) {
	sort(0, n-1, a[]);
}

// teraz to samo, tylko bez rekursji -- bottom up

void sort01(int & a[], int n) {

}