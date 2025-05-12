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

set<pair<string, int>> memo; // lampadas_acesas, idx_interruptor_atual para prevenir busca infinita 

void ativar_interruptor(bitset<1000> &lampadas, vector<bitset<1000>> interruptores, int idx_interruptor){
    bitset<1000> interruptor = interruptores[idx_interruptor];

    lampadas ^= interruptor;
}

int verificar(bitset<1000> lampadas, vector<bitset<1000>> interruptores){

    int idx = 0;
    int count = 0;
    while(1){
        if(memo.find({lampadas.to_string(),idx}) != memo.end()) return -1;
        memo.insert({lampadas.to_string(), idx});

        if(lampadas.none()) return count;

        ativar_interruptor(lampadas, interruptores, idx);
    
        count++;
        idx++;
        idx = idx % interruptores.size();
    }

    return -1;
}

int main(){ 

    int n,m;
    cin >> n >> m;

    bitset<1000> lampadas;
    lampadas.reset();
    vector<bitset<1000>> interruptores(n);

    int l; cin >> l;
    for(int i = 0; i<l; i++){
        int l_temp;
        cin >> l_temp;
        lampadas.set(--l_temp, 1);
    }

    for(int i = 0; i<n; i++){
        int k; cin >> k;
        for(int j=0; j<k; j++){
            int lampada; cin >> lampada;
            interruptores[i].set(--lampada, 1);
        }
    }

    cout << verificar(lampadas, interruptores) << endl;

    return 0;
}