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

    int t;
    cin >> t;

    // altura h
    // 1->2, 2->7, 3->15
    // cartas(1) = 2
    // cartas(h) = cartas(h-1) + 2h + h-1
    // cartas(h) = h(3h+1)/2

    // computar tudo q fica mais facil dps
    vecint cartas;
    int altura = 1;
    while(1){
        int cartas_necessarias = altura * (3*altura+1) / 2;
        if(cartas_necessarias > 1e9) break;
        cartas.pb(cartas_necessarias);
        altura++;
    }

    for(int i = 0; i<t; i++){
        int n;
        cin >> n;
        int ans = 0;
        while(n>=2){
            // comeca pelo maior
            auto it = upper_bound(cartas.begin(), cartas.end(), n);
            if (it == cartas.begin()) break;
            --it; // pegar o que cabe ainda
            n -= *it;
            ans++;
        }

        cout << ans << endl;

    }
    
    return 0;
}