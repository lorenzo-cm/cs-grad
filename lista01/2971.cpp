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

void print_hands(vector<vector<char>>& jogadores, int vez){
    int idx = 0;
    for(auto j : jogadores){
        for(auto c : j){
            cout << c << " ";
        }
        if(idx == vez) cout << "*";
        cout << endl;
        idx++;
    }
    cout << endl;
}


map<char, int> valores{
    {'C', 0},
    {'A', 1},
    {'2', 2},
    {'3', 3},
    {'4', 4},
    {'5', 5},
    {'6', 6},
    {'7', 7},
    {'8', 8},
    {'9', 9},
    {'D', 10},
    {'Q', 11},
    {'J', 12},
    {'K', 13},
};

bool can_pass_joker = false;
int joker_hand = -1;

char escolhe_carta(vector<vector<char>>& jogadores, int vez){
    vector<char> &cartas = jogadores[vez];
    vector<int> freq(13+1, 0);
    
    if(joker_hand == vez and can_pass_joker){
        can_pass_joker = false;
        cartas.erase(find(cartas.begin(), cartas.end(), 'C'));
        joker_hand++;
        joker_hand = joker_hand % jogadores.size();
        return 'C';
    }
    else{
        can_pass_joker = true;
    }


    for(int i = 0; i<cartas.size(); i++){
        freq[valores[cartas[i]]]++;
    }

    freq[0] = INF;

    int menor_freq = 5;
    int idx_menor_freq = -1;
    for(int i = 0; i<cartas.size(); i++){

        if(menor_freq > freq[valores[cartas[i]]]){
            menor_freq = freq[valores[cartas[i]]];
            idx_menor_freq = i;
        }
        else if(freq[valores[cartas[i]]] == menor_freq){
            if(valores[cartas[i]] < valores[cartas[idx_menor_freq]]){
                idx_menor_freq = i;
            }
        }
    }

    char return_carta = cartas[idx_menor_freq];
    cartas.erase(cartas.begin() + idx_menor_freq);

    return return_carta;
}

bool checar_vitoria(vector<char>& mao){
    return mao.size() == 4 && mao[0] == mao[1] && mao[1] == mao[2] && mao[2] == mao[3];
}

int loop(vector<vector<char>>& jogadores, int start){
    int vencedor = -1;
    int vez = start;

    for(int i = 0; i<jogadores.size(); i++){
        if(checar_vitoria(jogadores[i])) return i;
    }

    while(vencedor == -1){
        // cout << joker_hand << " | " << vez << endl;
        // cout << "canpass: " << can_pass_joker << endl;
        // print_hands(jogadores, vez);
        if(checar_vitoria(jogadores[vez])) return vez;

        char carta_passada = escolhe_carta(jogadores, vez);

        if(checar_vitoria(jogadores[vez])) return vez;

        vez++;
        vez = vez % jogadores.size();

        jogadores[vez].pb(carta_passada);
    }

    return vencedor;
}


int main(){ 

    int n, k; cin >>n >> k;

    vector<vector<char>> jogadores(n, vector<char>(4, ' '));

    for(int i = 0; i<n; i++){
        for(int j=0 ; j<4; j++){
            cin >> jogadores[i][j];
        }
    }

    joker_hand = k-1;
    jogadores[k-1].pb('C');

    cout << loop(jogadores, joker_hand)+1 << endl;
    
    return 0;
}