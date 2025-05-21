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

    ll a, b;
    cin >> a >> b;

    ll x, y, z;
    cin >> x >> y >> z;    

    ll precisa_amarelo = 2*x + y;
    ll precisa_azul = y + 3*z;

    ll qtd_minima_cristais_precisa = max(0LL, precisa_amarelo-a) + max(0LL, precisa_azul-b);

    cout << qtd_minima_cristais_precisa << endl;
    
    return 0;
}