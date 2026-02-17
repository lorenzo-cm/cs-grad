#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF   = 0x3f3f3f3f;
const ll  LINF = 0x3f3f3f3f3f3f3f3fll;

vecint encode(const string& word){
    unordered_map<char,int> base;
    unordered_map<char,int> occ;
    vecint res;

    for(char c : word){
        if(!base.count(c)) base[c] = c - 'A' + 1;
        res.pb(base[c] + occ[c] * 26);
        occ[c]++;
    }
    return res;
}

int min_removal_to_match(const vecint& a,const vecint& b){
    int n = a.size(), m = b.size();
    vector<vecint> lcs(n + 1, vecint(m + 1, 0));

    for(int i = 0;i < n;i++)
        for(int j = 0;j < m;j++)
            if(a[i] == b[j]){
                lcs[i + 1][j + 1] = lcs[i][j] + 1;
            }
            else{
                lcs[i + 1][j + 1] = max(lcs[i][j + 1], lcs[i + 1][j]);
            }

    return n + m - 2 * lcs[n][m];
}

bool try_match(int u,const vector<vecint>& graph,vector<bool>& visited,vector<int>& matched){
    for(int v : graph[u]){
        if(visited[v]) continue;
        visited[v] = true;

        if(matched[v] == -1 || try_match(matched[v], graph, visited, matched)){
            matched[v] = u;
            return true;
        }
    }
    return false;
}

int main(){ _
    int n, m;

    while(cin >> n >> m, n || m){
        vector<string> friends(n);
        vector<string> toys(m);
        for(int i = 0;i < n;i++) cin >> friends[i];
        for(int j = 0;j < m;j++) cin >> toys[j];

        vector<vecint> enc_friends;
        vector<vecint> enc_toys;
        for(const string& name : friends) enc_friends.pb(encode(name));
        for(const string& name : toys) enc_toys.pb(encode(name));

        vector<vecint> graph(n);
        for(int i = 0;i < n;i++)
            for(int j = 0;j < m;j++)
                if(min_removal_to_match(enc_friends[i], enc_toys[j]) % 5 == 0)
                    graph[i].pb(j);

        vector<int> matched(m, -1);
        int total_match = 0;
        
        for(int u = 0;u < n;u++){
            vector<bool> visited(m, false);
            if(try_match(u, graph, visited, matched)) total_match++;
        }

        double percent = (double)total_match * 100.0 / n;
        cout << fixed << setprecision(2) << "P = " << percent << endl;
    }

    return 0;
}
