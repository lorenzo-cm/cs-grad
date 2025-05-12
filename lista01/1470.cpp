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

map<vector<int>, int> memo;

pair<vector<int>, vector<int>> bigger_vector_first(vector<int> a, vector<int> b){
    if(a.size() >= b.size()) return {a, b};
    return {b, a};
}

vector<int> fazer_dobra(vector<int> fita, int index){

    vector<int> l(fita.begin(), fita.begin() + index);
    vector<int> r(fita.begin() + index, fita.end());

    reverse(r.begin(), r.end());

    int smaller_size = min(l.size(), r.size());
    int diff_size = abs(int(l.size() - r.size()));

    pair<vector<int>, vector<int>> result = bigger_vector_first(l, r);

    for(int i=0; i<smaller_size; i++){
        result.f[i+diff_size] += result.s[i]; 
    }

    return result.f;
}

int rec(vector<int> fita, vector<int> saida){
    if(memo.find(fita) != memo.end()) {
        return memo[fita];
    }
    if(fita == saida) return  1;
    if(fita.size() == 1){
        memo[fita] = 0;
        return 0;
    }

    for(int i=1; i<fita.size(); i++){
        vector<int> nova_fita = fazer_dobra(fita, i);
        if(rec(nova_fita, saida)) return 1;
    }

    memo[fita] = 0;
    return 0;
}

int main(){ _
    int n;
    while(cin >> n){
        vector<int> fita(n);
        for(int k = 0; k < n; k++) cin >> fita[k];

        int m; cin >> m;
        vector<int> saida(m);
        for(int k = 0; k < m; k++) cin >> saida[k];

        memo.clear();

        int suc1 = rec(fita, saida);
        reverse(fita.begin(), fita.end());
        int suc2 = rec(fita, saida);

        int suc = max(suc1, suc2);
        if(suc) cout << "S" << endl;
        else cout << "N" << endl;
    }
    
    return 0;
}