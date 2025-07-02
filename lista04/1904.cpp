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

int LIM = 1e7;

vector<unsigned> prefix_prime(){
    vecint is_prime(LIM + 1, 1);

    is_prime[0] = is_prime[1] = 0;
    for(int i = 2; i * 1LL * i <= LIM; i++){
        if(is_prime[i]){
            for(int j = i * i; j <= LIM; j += i){
                is_prime[j] = 0;
            }
        }            
    }
        
    vector<unsigned> pref(LIM + 1);
    pref[0] = 0;

    for(int i = 1; i <= LIM; i++){
        pref[i] = pref[i - 1] + is_prime[i];
    }

    return pref;
}

bool binom_par(unsigned n, unsigned r){
    return (r & n) == r;
}

int main() { _

    vector<unsigned> pref = prefix_prime();

    unsigned A, B;
    
    if(!(cin >> A >> B)) return 0;

    if(A == B){
        cout << "?\n";
        return 0;
    }

    unsigned L = min(A, B);
    unsigned R = max(A, B);
    unsigned k = R - L;
    unsigned m = pref[R] - (L ? pref[L - 1] : 0);


    if(m == 0){
        cout << "Bob\n";
        return 0;
    }

    unsigned n = (unsigned)(k) + m - 1;
    unsigned r = m - 1;
    bool odd = binom_par(n, r);

    cout << (odd ? "Alice\n" : "Bob\n");
    return 0;
}
