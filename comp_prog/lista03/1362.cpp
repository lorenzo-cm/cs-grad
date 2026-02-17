#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
// #define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

const int MAX = 39;

map<string, int> shirt_index = {
    {"XXL", 0},
    {"XL", 1},
    {"L", 2},
    {"M", 3},
    {"S", 4},
    {"XS", 5}
};

bool bfs(vector<vecint>& capacity, vector<vecint>& flow, vector<vecint>& adj, int s, int t, vector<int>& parent) {
    fill(parent.begin(), parent.end(), -1);
    queue<int> q;
    q.push(s);
    parent[s] = s;
    while(!q.empty()){
        int cur = q.front();
        q.pop();
        for(int next : adj[cur]) {
            if(parent[next] == -1 && capacity[cur][next] - flow[cur][next] > 0){
                parent[next] = cur;
                if (next == t) return true;
                q.push(next);
            }
        }
    }
    return false;
}

int edmonds_karp(vector<vecint>& capacity, vector<vecint>& flow, vector<vecint>& adj, int s, int t) {
    int maxFlow = 0;
    vector<int> parent(MAX);
    while(bfs(capacity, flow, adj, s, t, parent)){
        int aug_flow = INF;
        for(int u = t; u != s; u = parent[u]){
            aug_flow = min(aug_flow, capacity[parent[u]][u] - flow[parent[u]][u]);
        }
        for(int u = t; u != s; u = parent[u]) {
            flow[parent[u]][u] += aug_flow;
            flow[u][parent[u]] -= aug_flow;
        }
        maxFlow += aug_flow;
    }
    return maxFlow;
}

int main() { _
    // grafo bipartido
    // 6 tamanhos de camisa <-> M voluntarios
    // N multiplo de 6 -> N/6 para cada tipo
    // 0 a 5 -> camisas
    // 6 a 36 -> vols
    // 37 e 38 -> source e sink

    int T;
    cin >> T;
    for(int i = 0; i<T; i++){
        int N, M;
        cin >> N >> M;
        int size_shirts = N / 6;

        vector<vecint> capacity(MAX, vecint(MAX, 0));
        vector<vecint> flow(MAX, vecint(MAX, 0));
        vector<vecint> adj(MAX);

        int source = 37, sink = 38;

        for(int j = 0; j < 6; j++) {
            capacity[source][j] = size_shirts;
            adj[source].push_back(j);
            adj[j].push_back(source);
        }

        for(int j = 0; j < M; j++) {
            string s1, s2;
            cin >> s1 >> s2;
            int vol_node = 6 + j;

            for (string s : {s1, s2}) {
                int shirt_node = shirt_index[s];
                capacity[shirt_node][vol_node] = 1;
                adj[shirt_node].push_back(vol_node);
                adj[vol_node].push_back(shirt_node);
            }

            capacity[vol_node][sink] = 1;
            adj[vol_node].push_back(sink);
            adj[sink].push_back(vol_node);
        }

        int result = edmonds_karp(capacity, flow, adj, source, sink);
        cout << (result == M ? "YES" : "NO") << endl;
    }

    return 0;
}
