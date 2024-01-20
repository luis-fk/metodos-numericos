#include <stdio.h>
#include <cmath.h>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

double calculateDistance(double bodies[][2], int i, int j);
double calculateForce(double bodiesPosition[][2], double bodiesMass[], double distance[2][][], int i, int j, int k);
void atualize(double *x, double *y, double *vx, double *vy, double ax, double ay, double dt);

int main() {
    ifstream myfile ("data.txt");
    double number;
    int numberOfBodies, timeInterval, totalTime, currentTime {0}, iterations {0};
    double distancia, forca, acelaracao;

    myfile >> numberOfBodies;
    myfile >> timeInterval;
    myfile >> totalTime;

    struct body {
        double position[numberOfBodies][2] {};
        double velocty[numberOfBodies][2] {};
        double mass {};
        double distance[numberOfBodies][numberOfBodies][2] {};
        double force[numberOfBodies][numberOfBodies][2] {};
        double acceleration[numberOfBodies][numberOfBodies][2] {};
    };

    // double bodiesPosition[numberOfBodies][2];
    // double bodiesVelocity[numberOfBodies][2];
    // double bodiesMass[numberOfBodies];

    // double distance[numberOfBodies-1][numberOfBodies-1][2];
    // double force[numberOfBodies-1][numberOfBodies-1][2];
    // double acceleration[numberOfBodies-1][2];
    
    while (myfile >> number){
        for(int i = 0; i < numberOfBodies; i++)
            for(int j = 0; j < 7; j++){
                if (j < 3)
                    bodiesPosition[i][j] = number; 
                else if (j < 6)      
                    bodiesVelocity[i][j] = number;
                else 
                    bodiesMass[numberOfBodies] = number;
            }               
    }
    
    while (currentTime < totalTime)
    {
        /*calcula a distancia entre os corpos*/
        for (int i = 0; i <= numberOfBodies; i++) //iteration for each body
            for (int k = 0; k < 3; k++) // iteration for each coordinate (x, y, z)
                for (int j = 0; j <= numberOfBodies; j++) // iteration for interaction with each body
                    if (i != j)
                        distance[i][j][k] = calculateDistance(bodiesPosition, i, j);
                    else
                        distance[i][j][k] = -1;

        for (int i = 0; i <= numberOfBodies; i++) //iteration for each body
            for (int k = 0; k < 3; k++) // iteration for each coordinate (x, y, z)
                for (int j = 0; j <= numberOfBodies; j++) // iteration for interaction with each body
                    if (i != j)
                        force[i][j][k] = calculateDistance(bodiesPosition, bodiesMass, distance, i, j);
                    else
                        force[i][j][k] = -1;
    

        for (int i = 0; i <= numberOfBodies; i++) //iteration for each body
            for (int k = 0; k < 3; k++) // iteration for each coordinate (x, y, z)
                for (int j = 0; j <= numberOfBodies; j++) // iteration for interaction with each body
                    if (i != j)
                        acceleration[i][k] = force[i][j][k]
                    else
                        force[i][j][k] = -1;
        /*calcula a acelaracao causada pelas forcas nos eixos x e y para cada corpo*/
        ax0 = fgx0 / m0;
        ay0 = fgy0 / m0;

        ax1 = fgx1 / m1;
        ay1 = fgy1 / m1;

        ax2 = fgx2 / m2;
        ay2 = fgy2 / m2;

        /*funcao que atualiza os valores da posicao de velocidade de cada corpo*/
        atualize(&rx0, &ry0, &vx0, &vy0, ax0, ay0, dt);
        atualize(&rx1, &ry1, &vx1, &vy1, ax1, ay1, dt);
        atualize(&rx2, &ry2, &vx2, &vy2, ax2, ay2, dt);

        printf("%g %g %g %g %g %g\n", rx0, ry0, rx1, ry1, rx2, ry2);

        j = j + dt;
    }

return 0;
}


double calculateDistance(double bodiesPosition[][2], int i,int j){
    double x, y, z, distancia;

    x = bodiesPosition[i][0] - bodiesPosition[j][0];
    y = bodiesPosition[i][1] - bodiesPosition[j][1];
    z = bodiesPosition[i][2] - bodiesPosition[j][2];

    distancia = (x*x) + (y*y) + (z*z);
    return sqrt(distancia);
}

double calculateForce(double bodiesPosition[][2], double bodiesMass[], double distance[2][][]
             int i, int j, int k) {
    double mass1, mass2, distanceCubed, distanceSubtracted;
    mass1 = bodiesMass[i];
    mass2 = bodiesMass[j];
    distanceCubed = pow(distance[i][j][k], 3);
    distanceSubtracted = bodiesPosition[i][2]-bodiesPosition[j][2];

    return 6.6743e-11*((mass1*mass2)/distanceCubed)*distanceSubtracted;
                                    
}

void atualize(double *x, double *y, double *vx, double *vy, double ax, double ay, double dt)
{
    *vx = (*vx) + (dt * ax);
    *vy = (*vy) + (dt * ay);

    *y = (*y) + (dt * (*vy));
    *x = (*x) + (dt * (*vx));
}




