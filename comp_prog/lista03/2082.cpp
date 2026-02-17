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

struct edge {
    int v, flow, cap, rev;
};

class graph {
    int n;
    vector<vector<edge>> adj;
    vector<int> level;

public:
    graph(int n_) : n(n_), adj(n_), level(n_) {}

    void add_edge(int u, int v, int c) {
        edge a{v, 0, c, (int)adj[v].size()};
        edge b{u, 0, c, (int)adj[u].size()};
        adj[u].push_back(a);
        adj[v].push_back(b);
    }

    bool bfs(int s, int t) {
        fill(level.begin(), level.end(), -1);
        level[s] = 0;
        queue<int> q;
        q.push(s);
        while(!q.empty()){
            int u = q.front(); q.pop();
            for(auto &e : adj[u])
                if(level[e.v] < 0 && e.flow < e.cap){
                    level[e.v] = level[u] + 1;
                    q.push(e.v);
                }
        }
        return level[t] >= 0;
    }

    int send_flow(int u, int t, int flow, vector<int>& start){
        if(u == t) return flow;
        for(int &i = start[u]; i < (int)adj[u].size(); i++){
            edge &e = adj[u][i];
            if(level[e.v] == level[u] + 1 && e.flow < e.cap){
                int cur = min(flow, e.cap - e.flow);
                int temp = send_flow(e.v, t, cur, start);
                if(temp > 0){
                    e.flow += temp;
                    adj[e.v][e.rev].flow -= temp;
                    return temp;
                }
            }
        }
        return 0;
    }

    int max_flow(int s, int t){
        if(s == t) return INF;
        int total = 0;
        while(bfs(s, t)){
            vector<int> start(n, 0);
            while(int pushed = send_flow(s, t, INT_MAX, start))
                total += pushed;
        }
        return total == 0 ? INF : total;
    }

    void reset_flows(){
        for(auto &v : adj)
            for(auto &e : v) e.flow = 0;
    }
};

int main(){ _
    int T; 
    if(!(cin >> T)) return 0;
    while(T--){
        int n, m;
        cin >> n >> m;

        vector<vector<int>> cap(n, vector<int>(n, 0));
        for(int i = 0; i < m; i++){
            int u, v, c; cin >> u >> v >> c;
            u--; v--;
            cap[u][v] = cap[v][u] = c;
        }

        graph g(n);
        for(int i = 0; i < n; i++)
            for(int j = 0; j < i; j++)
                if(cap[i][j]) g.add_edge(i, j, cap[i][j]);

        int best = INF;
        for(int t = 1; t < n; t++){
            best = min(best, g.max_flow(0, t));
            g.reset_flows();
        }
        cout << best << endl;
    }
    return 0;
}
