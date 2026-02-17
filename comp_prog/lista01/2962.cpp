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

        Sensor(int x_, int y_, int r_){
            this->r = r_;
            this->x = x_;
            this->y = y_;
        }
        Sensor(){};
};

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
    return x+r >= m;
}

bool top_border(int x, int y, int r){
    return  y+r >= n;
}

bool bottom_border(int x, int y, int r){
    return  y-r <= 0;
}

bool sensors_intercept(Sensor &s1, Sensor &s2){
    return (pow((s1.x-s2.x), 2) + pow((s1.y-s2.y), 2)) <= (s1.r + s2.r)*(s1.r + s2.r);
}

int main(){ _

    cin >> m >> n >> k;
    int tx, ty, tr;

    vector<int> union_find(k+4);
    for(int i = 0; i<k+4; i++) union_find[i] = i;
    vector<Sensor> sensors(k);

     
    for(int i = 0; i < k; i++){
        cin >> tx >> ty >> tr;

        sensors[i] = Sensor(tx, ty, tr);

        if(left_border(tx, ty, tr))  union_func(union_find, 0, i+4);
        if(top_border(tx, ty, tr))  union_func(union_find, 1, i+4);
        if(right_border(tx, ty, tr))  union_func(union_find, 2, i+4);
        if(bottom_border(tx, ty, tr))  union_func(union_find, 3, i+4);
    }

    for(int i=0; i<k; i++){
        for(int j=i+1; j<k; j++){
            if(sensors_intercept(sensors[i], sensors[j])) union_func(union_find, i+4, j+4);
        }
    }

    if(find(union_find, 0) == find(union_find, 2) or 
       find(union_find, 0) == find(union_find, 3) or
       find(union_find, 1) == find(union_find, 3) or
       find(union_find, 1) == find(union_find, 2))
        cout << "N" << endl;

    else
        cout << "S" << endl;
    
    return 0;
}