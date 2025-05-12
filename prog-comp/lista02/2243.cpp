#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

int main(){ _

    int n; cin >> n;

    vecint values(n);

    for(int i = 0; i<n; i++){
        cin >> values[i];
    }


    vecint results_l(n, 0);
    vecint results_r(n, 0);


    // left to right
    results_l[0] = 1;
    for(int i = 1; i<n; i++){
        results_l[i] = min(
                        values[i], // altura
                        results_l[i-1] + 1 // escadinha a partir do anterior
                    );
    }

    // right to left
    results_r[n-1] = 1;
    for(int i = n-2; i>=0; i--){
        results_r[i] = min(
                        values[i], // altura
                        results_r[i+1] + 1 // escadinha a partir do anterior
                    );
    }

    int max_val = 0;
    for(int i = 0; i<n; i++){
        if(min(results_l[i], results_r[i]) > max_val) max_val = min(results_l[i], results_r[i]);
    }

    cout << max_val << endl;

    return 0;
}