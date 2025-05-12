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

int dijkstra_peso_vertice(vector<vector<int>> adj, vector<int> pesos, int partida, int destino){
    vector<int> dist(pesos.size(), INF);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    dist[partida] = pesos[partida];
    pq.push({pesos[partida], partida});

    while(!pq.empty()){
        pair<int, int> p_temp = pq.top();
        int curr = p_temp.s; 
        pq.pop();

        for (int v : adj[curr]) { 
            if (dist[v] > dist[curr] + pesos[v]) {
                dist[v] = dist[curr] + pesos[v];
                pq.push({dist[v], v});
            }
        }
    }


    return dist[destino];
}


int main(){ _

    int n, m, k;
    double p;

    while(cin >> n >> m >> k >> p){

        vector<vector<int>> adj(n);

        for(int i = 0; i<m; i++){
            int temp1, temp2;
            cin >> temp1 >> temp2;
            adj[temp1-1].pb(temp2-1);
            adj[temp2-1].pb(temp1-1);
        }

        int a;
        cin >> a;

        vector<int> atir(n);

        for(int i=0; i<a; i++){
            int temp;
            cin >> temp;
            atir[temp-1]++;
        }

        int partida, destino;
        cin >> partida >> destino;
        partida--;
        destino--;
        
        int peso_min = dijkstra_peso_vertice(adj, atir, partida, destino);

        if (peso_min > k) {
            cout << fixed << setprecision(3) << 0.000 << endl;
        } else {
            cout << fixed << setprecision(3) << pow(p, peso_min) << endl;
        }
    }

    return 0;
}