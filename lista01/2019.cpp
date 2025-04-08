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


int m, n, k;

class Sensor{
    public:
        int r, x, y;

        Sensor(int r_, int x_, int y_){
            this->r = r_;
            this->x = x_;
            this->y = y_;
        }
};

vector<pair<int, Sensor>> union_find;
set<int> left, top, right, bottom;

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



bool left_border(int x, int y, int r){
    return x-r <= 0;
}

bool right_border(int x, int y, int r){
    return x+r >= n;
}

bool top_border(int x, int y, int r){
    return  y+r >= m;
}

bool bottom_border(int x, int y, int r){
    return  y-r <= 0;
}


int main(){ _

    cin >> m >> n >> k;
    int tx, ty, tr;

     
    for(int i = 0; i < k; i++){
        cin >> tx >> ty >> tr;
        union_find.push_back({i, Sensor(tr, tx, ty)});

        if(left_border(tx, ty, tr)) left.insert(i);

    }

    for(int i=0; i<k; i++){
        for(int j=0; j<k; j++){

        }
    }


    
    return 0;
}