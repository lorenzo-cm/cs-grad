#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF  = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;


void sieve(vecint& primes, bitset<20'000'000 + 1>& is_composite, int lim){
    for(int i = 2; 1LL * i * i <= lim; ++i){
        if(!is_composite[i]){
            for(int j = i * i; j <= lim; j += i){
                is_composite[j] = 1;
            }
        }
    }
        

    for(int i = 2; i <= lim; ++i){
        if(!is_composite[i]){
            primes.pb(i);
        }
    }
}

int main(){ _
    bitset<20'000'000 + 1> is_composite;
    vecint primes;
    sieve(primes, is_composite, 20'000'000);

    int T;
    if(!(cin >> T)) return 0;

    while(T--){
        int N; cin >> N;

        unordered_set<int> S;
        S.reserve(N * 2);

        for(int i = 0; i < N; ++i){
            int x; cin >> x;
            S.insert(x);
        }

        if(!S.count(1)){
            cout << 0 << endl;
            continue;
        }

        for(int p : primes){
            if(!S.count(p)){
                cout << p - 1 << endl;
                break;
            }
        }
    }

    return 0;
}
