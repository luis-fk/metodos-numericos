#include <iostream>
#include <cmath>
#include <fstream>
#include <chrono>
using namespace std;

struct bodyInfo {
    double position[3] {0};
    double velocity[3] {0};
    double mass {0};
};

double calculateDistance(bodyInfo *body, int body1, int body2, double factor);
void RungeKuta44(bodyInfo *body, double timeInterval);
void phiFunction(bodyInfo *body, double timeInterval, int body1, int body2, 
                   int body3, int coordinate);
double velocity(double factor, int body1, int body2, int body3, bodyInfo *body, int coordinate);
double calculateDistance(bodyInfo *body, int body1, int body2, double factor);

int main() {
    auto start_time = std::chrono::high_resolution_clock::now();

    int dataRegister {0};
    double number {0}, timeInterval {0}, steps {0}, currentTime {0};

    /* Os primeiros dados a serem lidos sao o numero de corpos,
       o intervalo de tempo (delta T) e o numero de passos (iteracoes) */
    ifstream data ("data.txt");
    data >> timeInterval;
    data >> steps;
    data >> dataRegister;

    /* Creates an array of bodyInfo of the size of numberOfBodies */
    bodyInfo* body = new bodyInfo[3];
    
    /* Stores the initial data for position, velocty and mass of each body */
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            data >> number;
            body[i].position[j] = number;
        }

        for(int j = 0; j < 3; j++) {
            data >> number;
            body[i].velocity[j] = number;
        }

        data >> number;
        body[i].mass = number;
    }             

    data.close();

    ofstream output ("output.txt");
    output << scientific;

    for (int i = 0; i < 3; i++) {
        for (int k = 0; k < 3; k++) {
            output << body[i].position[k] << " ";
        }
    }

    output << "\n";
    for (int i = 1; i < steps; i++) {
        currentTime += timeInterval*i;
        RungeKuta44(body, timeInterval);

        // RungeKuta44(body, timeInterval, 1);
        
        if (i % dataRegister == 0) {
            for (int i = 0; i < 3; i++) {
                for (int k = 0; k < 3; k++){
                    output << body[i].position[k] << " ";

                    // if (abs(body[i].position[k]) > 10)
                    //     return 0;
                }
            }
            output << "\n";
        }
    }

    delete[] body;
    output.close();

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::duration<double>>(end_time - start_time);
    std::cout << "Time taken by function: " << duration.count() << " seconds" << std::endl;

    return 0;
}

void RungeKuta44(bodyInfo *body, double timeInterval) {
    /* Here, one body [i] will be selected to have its distance calculated compared
       to every other body in the system */
    for (int i = 0; i < 3; i++) {
        /* Iteration for each on of the coordinates (x, y, z) */
        for (int k = 0; k < 3; k++) {
            if (i == 0) {
                phiFunction(body, timeInterval, 0, 1, 2, k);
            }
            else if (i == 1) {
                phiFunction(body, timeInterval, 1, 0, 2, k);
            }
            else if (i == 2) {
                phiFunction(body, timeInterval, 2, 0, 1, k);
            }    
        }
    }    

    return;                          
}

void phiFunction(bodyInfo *body, double timeInterval, int body1, int body2, 
                   int body3, int coordinate) {
    double k1, k2, k3, k4, phi;

    k1 = velocity(0, body1, body2, body3, body, coordinate);
    k2 = velocity(k1*(timeInterval/2), body1, body2, body3, body, coordinate);
    k3 = velocity(k2*(timeInterval/2), body1, body2, body3, body, coordinate);
    k4 = velocity(k3*timeInterval, body1, body2, body3, body, coordinate);
    phi = (k1 + 2*k2 + 2*k3 + k4)/6;

    body[body1].velocity[coordinate] = body[body1].velocity[coordinate] + timeInterval*phi;
    body[body1].position[coordinate] = body[body1].position[coordinate] + timeInterval*body[body1].velocity[coordinate];
}

double velocity(double factor, int body1, int body2, int body3, bodyInfo *body, int coordinate) {
    double distanceCubed1, distanceCubed2, distanceSubtracted1, 
           distanceSubtracted2, mass2, mass3;

    distanceSubtracted1 = (body[body2].position[coordinate] + factor) - 
                          (body[body1].position[coordinate] + factor); 
    distanceSubtracted2 = (body[body3].position[coordinate] + factor) - 
                          (body[body1].position[coordinate] + factor); 

    mass2 = body[body2].mass;
    mass3 = body[body3].mass;
    
    distanceCubed1 = pow(calculateDistance(body, body1, body2, factor), 3);
    distanceCubed2 = pow(calculateDistance(body, body1, body3, factor), 3);

    return -6.67430e-11*(((mass2*distanceSubtracted1)/(distanceCubed1)) +
                         ((mass3*distanceSubtracted2)/(distanceCubed2)));
}

double calculateDistance(bodyInfo *body, int body1, int body2, double factor) {
    double x, y, z;

    x = (body[body1].position[0] + factor) - (body[body2].position[0] + factor);
    y = (body[body1].position[1] + factor) - (body[body2].position[1] + factor);
    z = (body[body1].position[2] + factor) - (body[body2].position[2] + factor);
    
    return sqrt((x*x) + (y*y) + (z*z));
}
