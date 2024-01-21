#include <iostream>
#include <cmath>
#include <fstream>
#include <chrono>
using namespace std;

struct bodyInfo {
    double position[3] {0};
    double velocity[3] {0};
    double mass {0};
    double *distance {0};
    double force[3] {0};
    double acceleration[3] {0};
};

void calculateDistance(bodyInfo *body, int numberOfBodies);
void calculateForce(bodyInfo *body, int numberOfBodies);
void calculateAcceleration(bodyInfo *body, int numberOfBodies);
void update(bodyInfo *body, double timeInterval, int numberOfBodies);

int main() {
    auto start_time = std::chrono::high_resolution_clock::now();

    int numberOfBodies {0};
    double number {0}, timeInterval {0}, steps {0};

    /* Os primeiros dados a serem lidos sao o numero de corpos,
       o intervalo de tempo (delta T) e o numero de passos (iteracoes) */
    ifstream data ("data.txt");
    data >> numberOfBodies;
    data >> timeInterval;
    data >> steps;

    /* Creates an array of bodyInfo of the size of numberOfBodies */
    bodyInfo* body = new bodyInfo[numberOfBodies];
    
    /* Creates and initializes de distance double for each body */
    for (int i = 0; i < numberOfBodies; ++i) {
        body[i].distance = new double[numberOfBodies];

        for (int j = 0; j < 3; ++j) {
            body[i].distance[j] = 0;
        }
    }

    /* Stores the initial data for position, velocty and mass of each body */
    for(int i = 0; i < numberOfBodies; i++) {
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

    for (int i = 1; i < steps; i++) {
        calculateDistance(body, numberOfBodies);

        calculateForce(body, numberOfBodies);

        calculateAcceleration(body, numberOfBodies);

        update(body, timeInterval, numberOfBodies);
        
        for (int i = 0; i < numberOfBodies; i++) {
            for (int k = 0; k < 3; k++){
                output << body[i].position[k] << " ";
            }
        }
        output << "\n";
        
        // if (abs(body[0].distance[1]) > 30)
        //     return 0;
    }

    for (int i = 0; i < numberOfBodies; ++i) {
        delete body[i].distance;
    }
    delete[] body;
    output.close();

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::duration<double>>(end_time - start_time);
    std::cout << "Time taken by function: " << duration.count() << " seconds" << std::endl;

    return 0;
}

/*calcula a distancia entre os corpos*/
void calculateDistance(bodyInfo *body, int numberOfBodies) {
    double x, y, z;

    /* Here, one body [i] will be selected to have its distance calculated compared
       to every other body in the system */
    for (int i = 0; i < numberOfBodies; i++) {
        /* This is where body [i] will have its distance calculated in respect
            to all the other [j] bodies */
        for (int j = i + 1; j < numberOfBodies; j++) {
            x = body[i].position[0] - body[j].position[0];
            y = body[i].position[1] - body[j].position[1];
            z = body[i].position[2] - body[j].position[2];
            
            body[i].distance[j] = sqrt((x*x) + (y*y) + (z*z));
            body[j].distance[i] = body[i].distance[j];
        }
    }

    return;       
}

void calculateForce(bodyInfo *body, int numberOfBodies) {
    double mass1, mass2, distanceCubed, distanceSubtracted;

    /* Here, one body [i] will be selected to have its distance calculated compared
       to every other body in the system */
    for (int i = 0; i < numberOfBodies; i++) {
        /* Iteration for each on of the coordinates (x, y, z) */
        for (int k = 0; k < 3; k++) {
            /* This is where body [i] will have its distance calculated in respect
               to all the other [j] bodies */
            body[i].force[k] = 0;
            for (int j = 0; j < numberOfBodies; j++) {
                if (i != j) {
                    mass1 = body[i].mass;
                    mass2 = body[j].mass;
                    distanceCubed = pow(body[i].distance[j], 3);
                    distanceSubtracted = body[j].position[k] - body[i].position[k];

                    body[i].force[k] += 6.6743e-11*((mass1*mass2)/distanceCubed)*distanceSubtracted;
                }
            }
        }
    }    

    return;                          
}

void calculateAcceleration(bodyInfo *body, int numberOfBodies) {
    /* Calculate the acceleration of everybody on x, y and z */
    for (int i = 0; i < numberOfBodies; i++) {
        for (int k = 0; k < 3; k++) {
            body[i].acceleration[k] = body[i].force[k] / body[i].mass;
        }
    }

    return;   
}

void update(bodyInfo *body, double timeInterval, int numberOfBodies) {
    /* Updates the velocity and position of each body using a basic Euler method
       of step integration */
    for (int i = 0; i < numberOfBodies; i++) {
        for (int k = 0; k < 3; k++) {
            body[i].velocity[k] = body[i].velocity[k] + (timeInterval * body[i].acceleration[k]);
            body[i].position[k] = body[i].position[k] + (timeInterval * body[i].velocity[k]);
        }
    }

    return;   
}