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

int main(){ _

    int n, m; cin >> n >> m;

    vector<vector<pair<int, int>>> adjw(n);

    int u,v,w;
    for(int i=0; i<m; i++){
        cin >> u >> v >> w;
        adjw[u-1].pb({w, v-1});
        adjw[v-1].pb({w, u-1});
    }

    int serv; cin >> serv; serv--;

    vector<int> dist(n, INF);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    dist[serv] = 0;
    pq.push({0, serv});

    while(!pq.empty()){
        pair<int, int> p_temp = pq.top();
        int vert_curr = p_temp.s; 
        pq.pop();

        for (pair<int, int> p_temp2 : adjw[vert_curr]) {
            int cost_neigh = p_temp2.f;
            int vert_neigh = p_temp2.s; 
            if (dist[vert_neigh] > dist[vert_curr] + cost_neigh) {
                dist[vert_neigh] = dist[vert_curr] + cost_neigh;
                pq.push({dist[vert_neigh], vert_neigh});
            }
        }
    }

    int max_ping = 0, min_ping = INF;

    for (int i = 0; i < n; i++) {
        if (i == serv) continue;
        max_ping = max(max_ping, dist[i]);
        min_ping = min(min_ping, dist[i]);
    }

    cout << max_ping - min_ping << endl;
    
    return 0;
}