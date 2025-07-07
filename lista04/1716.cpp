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

ll gcd_ext(ll a, ll b, ll& x, ll& y){
    if(!b){
        x = 1;
        y = 0;
        return a;
    }

    ll x1, y1;
    ll g = gcd_ext(b, a % b, x1, y1);

    x = y1;
    y = x1 - (a / b) * y1;

    return g;
}

ll mod_inv(ll a, ll m){
    ll x, y;
    ll g = gcd_ext(a, m, x, y);

    if (g != 1) return -1;

    x %= m;
    if (x < 0) x += m;

    return x;
}

ll mod_pow(ll base, ll exp, ll mod){
    ll res = 1 % mod;
    base %= mod;
    while(exp){
        if(exp & 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}

int main(){ _
    ll N, E, C;

    if(!(cin >> N >> E >> C)) return 0;

    ll P = -1, Q = -1;
    if (N % 2 == 0){
        P = 2;
        Q = N / 2;
    }
    else {
        for(ll p = 3; p * p <= N; p += 2){
            if(N % p == 0){
                P = p;
                Q = N / p; break;
            }
        }
    }

    ll phi = (P - 1) * (Q - 1);
    ll D = mod_inv(E, phi);
    ll M = mod_pow(C, D, N);

    cout << M << endl;
    return 0;
}
