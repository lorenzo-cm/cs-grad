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


bool possivel(vector<int> &pipoca, ll m, ll c, int t){
    // m é o tempo que eles tem
    // c = qtd de competidores na equipe
    // t = taxa pipoca por segundo para cada competidor
    int competidores = 0;
    ll pipocas_comidas_em_m_indiv = m * t;
    for(int p : pipoca){
        if(competidores >= c) return false;
        if(pipocas_comidas_em_m_indiv >= p){
            pipocas_comidas_em_m_indiv -= p;
        }
        else{
            competidores++;
            pipocas_comidas_em_m_indiv = m*t;
            pipocas_comidas_em_m_indiv -= p;
            if(pipocas_comidas_em_m_indiv < 0) return false;
        }
    }
    return true;
}


int main(){ _
    int n, c, t;
    cin >> n >> c >> t;

    vector<int> pipoca(1e5 + 10);

    for(int i=0; i<n; i++){
        cin >> pipoca[i];
    }

    int l = 0;
    int r = 1e9 + 10;

    // busca binaria
    while(l < r){
        int m = (l+r)/2;
        if(!possivel(pipoca, m, c, t)) l = m+1;
        else r = m;
    }

    cout << r << endl;
    
    return 0;
}