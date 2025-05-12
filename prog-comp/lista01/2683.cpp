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


int find(vector<int> &union_find, int x){
    if(union_find[x] != x) union_find[x] = find(union_find, union_find[x]);
    return union_find[x];
}

bool union_func(vector<int>& union_find, int x, int y) {
    int root_x = find(union_find, x);
    int root_y = find(union_find, y);

    if(root_x == root_y) return false;

    else if (root_x < root_y){
        union_find[root_y] = root_x;
    }
    else{
        union_find[root_x] = root_y;
    }

    return true;
}


bool compara_cres(const tuple<int, int, int>& a, const tuple<int, int, int>& b) {
    return get<0>(a) < get<0>(b);
}

bool compara_decres(const tuple<int, int, int>& a, const tuple<int, int, int>& b) {
    return get<0>(a) > get<0>(b);
}

int min_st(vector<int> union_find, vector<tuple<int, int, int>> list_edges){
    sort(list_edges.begin(), list_edges.end(), compara_cres);
    
    int total = 0;

    for(auto [w, u, v] : list_edges){
        if(union_func(union_find, u, v)){
            total += w;
        }
    }

    return total;
}

int max_st(vector<int> union_find, vector<tuple<int, int, int>> list_edges){
    sort(list_edges.begin(), list_edges.end(), compara_decres);
    
    int total = 0;

    for(auto [w, u, v] : list_edges){
        if(union_func(union_find, u, v)){
            total += w;
        }
    }

    return total;
}


int main(){ _

    int n; cin >> n;

    vector<vector<pair<int, int>>> adj(n);
    vector<tuple<int, int, int>> list_edges(n);
    vector<int> union_find(n);

    int u, v, w;
    for(int i=0; i<n; i++){
        cin >> u >> v >> w;
        adj[u].pb({v, w});
        // adj[v].pb({u, w});

        list_edges[i] = {w, u, v};

        union_find[i] = i;
    }

    cout << max_st(union_find, list_edges) << endl;
    cout << min_st(union_find, list_edges) << endl;

    return 0;
}