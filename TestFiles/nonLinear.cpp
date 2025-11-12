#include <bits/stdc++.h>
using namespace std;

void for1(){
     int x = 0, a, b, c, n, m;
    cout << "enter the values for a,b,c and power of a and b: ";
    cin >> a >> b >> c >> n >> m;

    cout << "function is f(x)= " << a << "x^" << n <<  " +(" << b << ")x^" << m << " +(" << c <<")" <<endl;

    int func1 = 0, func2 = INT_MAX, funcidx = 0;

    
    for (int i = 0; i <= 5; i++) {
        int p = 1, q = 1;
        for (int j = 0; j < n; j++) {
            p *= i;
        }
        for (int j = 0; j < m; j++) {
            q *= i;
        }
        func1 = a * p + (b * q) + c;
        if (abs(func1) < abs(func2)) { 
            func2 = func1;
            funcidx = i;
        }
    }

    
    float ans[10]; 
    ans[0] = funcidx;
    float xval = ans[0];

    for (int i = 1; i < 5; i++) {
        float fx = a * pow(xval, n) + b * pow(xval, m) + c;
        float dfx = (a * n * pow(xval, n - 1)) + (b * m * pow(xval, m - 1)); 

        if (dfx == 0) break; 

        ans[i] = xval - (fx / dfx);

        if (fabs(ans[i] - xval) <=0) { 
            xval = ans[i];
            break;
        }
        xval = ans[i];
    }

    cout << "final x val = " << xval << endl;
}


 double Log(double n){
    if(n==0){
        return 1;
    }
   return log10(n);
 }
 
void for2(){
     double a, b;
    cout << "enter the values for a,b : ";
    cin >> a >> b;
cout<<"function f(x) is : "<<a<<"x + ("<<b<<") = log10(x)"<<endl;

 int func1 = 0, func2 = INT_MAX, funcidx = 0;

    for (int i = 0; i <= 5; i++) {
        int p = 1, q = 1;
       func1=(a*i)+(b)-Log(i);
 if (abs(func1) < abs(func2)) { 
            func2 = func1;
            funcidx = i;
        }
    }


     float ans[10]; 
    ans[0] = funcidx;
    float xval = ans[0];

    for (int i = 1; i < 5; i++) {
        float fx = (a*xval)+(b)-(Log(xval));
          float dfx = a - 1.0 / (xval * log(10));

        if (dfx == 0) break; 

        ans[i] = xval - (fx / dfx);

        if (fabs(ans[i] - xval) <=0) { 
            xval = ans[i];
            break;
        }
        xval = ans[i];
    }

    cout << "final x val = " << xval << endl;
}



int main() {
   
cout<<"enter the sl. number which type of equation ?"<<endl;
cout<<"1. Quadtratic or cubic "<<endl;
cout<<"2. logerithemic"<<endl;
int sl;
cin>>sl;
if(sl==1){
 for1();
}else if(sl==2){
for2();
}else{
    cout<<"you have entered wrong input";
}

    return 0;
}



