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

const ll MOD = 1'000'000LL;

struct Mat{
    ll a, b, c, d;
};

Mat mul(const Mat& x, const Mat& y){
    return{
        (x.a * y.a + x.b * y.c) % MOD,
        (x.a * y.b + x.b * y.d) % MOD,
        (x.c * y.a + x.d * y.c) % MOD,
        (x.c * y.b + x.d * y.d) % MOD
    };
}

Mat mpow(Mat base, unsigned long long e){
    Mat res{1, 0, 0, 1};
    while(e){
        if(e & 1) res = mul(res, base);
        base = mul(base, base);
        e >>= 1;
    }
    return res;
}

int main(){ _
    unsigned long long N, K, L;
    while(cin >> N >> K >> L){
        unsigned long long M = N / 5ULL;
        ll k = K % MOD;
        ll l = L % MOD;
        ll ans;
        if(M == 0) ans = 1;
        else if(M == 1) ans = k;
        else{
            Mat A {k, l, 1, 0};
            Mat P = mpow(A, M - 1);
            ans = (P.a * k + P.b) % MOD;
        }
        cout << setw(6) << setfill('0') << ans << endl;
    }
    return 0;
}
