#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

bool check_despojado(ll n){
    if (n < 2) return false;
    bool primo = true;
    for (ll i = 2; i <= sqrt(n); i++) {
        if(n % (i*i) == 0) return false;
        if(n % i == 0) primo = false;
    }
    return !primo;
}


int main(){ _

    ll n; cin >> n;

    ll ans = 0;
    for(ll i = 1; i<=sqrt(n); i++){
        if(n % i == 0){
            if(check_despojado(i))
                ans++;

            if(i != n/i and check_despojado(n/i)) 
                ans++;
        }
    }
    cout << ans << endl;
    
    return 0;
}