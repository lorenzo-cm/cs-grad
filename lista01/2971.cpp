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


void melhor_jogada(vector<vector<char>>& jogadores, int vez){
    vector<char> cartas = jogadores[vez];

    sort(cartas.begin(), cartas.end());

}

int checar_vitoria(vector<vector<char>>& jogadores){
    for(int i = 0; i<jogadores.size(); i++){
        if(jogadores[i][0] == jogadores[i][1] and
           jogadores[i][1] == jogadores[i][2] and
           jogadores[i][2] == jogadores[i][3])
            return i;
    }
    return -1;
}


int loop(vector<vector<char>>& jogadores){
    int vencedor = -1;
    int vez = 0;
    while(vencedor == -1){
        vez = vez % jogadores.size();
        
        if(checar_vitoria(jogadores) != -1) return checar_vitoria(jogadores);

        melhor_jogada(jogadores, vez);

        vez++;
    }

    return vencedor;
}


int main(){ _

    int n, k; cin >>n >> k;

    vector<vector<char>> jogadores(n, vector<char>(4, ' '));

    for(int i = 0; i<n; i++){
        for(int j=0 ; j<4; j++){
            cin >> jogadores[i][j];
        }
    }





    
    return 0;
}