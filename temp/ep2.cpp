#include <stdio.h>
#include <math.h>
#include <iostream>

double dist(double p1x, double p1y, double p2x, double p2y);
double forca(char c, int i, double x0, double y0, double m0, double x1, double y1, double m1, double x2, double y2, double m2,
             double dist1, double dist2);
void atualize(double *x, double *y, double *vx, double *vy, double ax, double ay, double dt);

int main()
{
    double rx0, ry0, vx0, vy0, m0;
    double rx1, ry1, vx1, vy1, m1;
    double rx2, ry2, vx2, vy2, m2;
    double dt, T;
    scanf("%lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf", &rx0, &ry0, &vx0, &vy0, &m0,
           &rx1, &ry1, &vx1, &vy1, &m1, &rx2, &ry2, &vx2, &vy2, &m2, &T, &dt);

    double j = dt;
    double dist_c12, dist_c01, dist_c02, fgx0, fgy0, fgx1, fgy1, fgx2, fgy2;
    double ax0, ay0, ax1, ay1, ax2, ay2;

    printf("%g %g %g %g %g %g\n", rx0, ry0, rx1, ry1, rx2, ry2);

    while (j < T)
    {
        /*calcula a distancia entre os corpos 0, 1 e 2*/
        dist_c01 = dist(rx0, ry0, rx1, ry1);
        dist_c02 = dist(rx0, ry0, rx2, ry2);
        dist_c12 = dist(rx1, ry1, rx2, ry2);
        printf("dist_c01: %g\n dist_c02: %g\n", dist_c01, dist_c02);

        /*funcao 'forca' calcula a forca gravitacional em cada um dos corpos nas coordenadas x e y*/
        fgx0 = forca('x', 0, rx0, ry0, m0, rx1, ry1, m1, rx2, ry2, m2, dist_c01, dist_c02);
        fgy0 = forca('y', 0, rx0, ry0, m0, rx1, ry1, m1, rx2, ry2, m2, dist_c01, dist_c02);
        printf("fgx0: %g\n fgy0: %g\n", fgx0, fgy0);
        fgx1 = forca('x', 1, rx0, ry0, m0, rx1, ry1, m1, rx2, ry2, m2, dist_c01, dist_c12);
        fgy1 = forca('y', 1, rx0, ry0, m0, rx1, ry1, m1, rx2, ry2, m2, dist_c01, dist_c12);

        fgx2 = forca('x', 2, rx0, ry0, m0, rx1, ry1, m1, rx2, ry2, m2, dist_c02, dist_c12);
        fgy2 = forca('y', 2, rx0, ry0, m0, rx1, ry1, m1, rx2, ry2, m2, dist_c02, dist_c12);
        
        /*calcula a acelaracao causada pelas forcas nos eixos x e y para cada corpo*/
        ax0 = fgx0 / m0;
        ay0 = fgy0 / m0;
        printf("ax0: %g\n ay0: %g\n", ax0, ay0);

        ax1 = fgx1 / m1;
        ay1 = fgy1 / m1;

        ax2 = fgx2 / m2;
        ay2 = fgy2 / m2;

        /*funcao que atualiza os valores da posicao de velocidade de cada corpo*/
        atualize(&rx0, &ry0, &vx0, &vy0, ax0, ay0, dt);
        atualize(&rx1, &ry1, &vx1, &vy1, ax1, ay1, dt);
        atualize(&rx2, &ry2, &vx2, &vy2, ax2, ay2, dt);

        printf("ax0: %g\n ay0: %g\n", rx0, ry0);
        printf("%g %g %g %g %g %g\n", rx0, ry0, rx1, ry1, rx2, ry2);

        j = j + dt;
    }

return 0;
}


double dist(double p1x, double p1y, double p2x, double p2y) /*distancia entre os corpos 0 e 1, 0 e 2, e 1 e 2.*/
{
    double px, py, pt;

    px = p1x - p2x;
    py = p1y - p2y;

    pt = (px*px) + (py*py);
    pt = sqrt(pt);

    return pt;
}

double forca(char c, int i, double x0, double y0, double m0, double x1, double y1, double m1, double x2, double y2, double m2,
             double dist1, double dist2)
{
    double f_grav1, f_grav2;

    if(c == 'x' && i == 0)/*forca da gravidade dos corpos 1 e 2 sobre o corpo 0 na coordenada x*/
    {
        f_grav1 = 6.6743e-11*((m0*m1)/((dist1)*(dist1)))*((x1-x0)/(dist1));
        f_grav2 = 6.6743e-11*((m0*m2)/((dist2)*(dist2)))*((x2-x0)/(dist2));

        return f_grav1 + f_grav2;
    }
    else if(c == 'y' && i == 0)/*forca da gravidade dos corpos 1 e 2 sobre o corpo 0 na coordenada y*/
    {
        f_grav1 = (6.6743e-11*((m0*m1)/((dist1)*(dist1))))*((y1-y0)/(dist1));
        f_grav2 = (6.6743e-11*((m0*m2)/((dist2)*(dist2))))*((y2-y0)/(dist2));

        return f_grav1 + f_grav2;

    }
    else if(c == 'x' && i == 1)/*forca da gravidade dos corpos 0 e 2 sobre o corpo 1 na coordenada x*/
    {
        f_grav1 = (6.6743e-11*((m1*m0)/((dist1)*(dist1))))*((x0-x1)/(dist1));
        f_grav2 = (6.6743e-11*((m1*m2)/((dist2)*(dist2))))*((x2-x1)/(dist2));

        return f_grav1 + f_grav2;
    }
    else if(c == 'y' && i == 1)/*forca da gravidade dos corpos 0 e 2 sobre o corpo 1 na coordenada y*/
    {
        f_grav1 = (6.6743e-11*((m1*m0)/((dist1)*(dist1))))*((y0-y1)/(dist1));
        f_grav2 = (6.6743e-11*((m1*m2)/((dist2)*(dist2))))*((y2-y1)/(dist2));

        return f_grav1 + f_grav2;
    }
    else if(c == 'x' && i == 2)/*forca da gravidade dos corpos 0 e 1 sobre o corpo 2 na coordenada x*/
    {
        f_grav1 = (6.6743e-11*((m2*m0)/((dist1)*(dist1))))*((x0-x2)/(dist1));
        f_grav2 = (6.6743e-11*((m2*m1)/((dist2)*(dist2))))*((x1-x2)/(dist2));

        return f_grav1 + f_grav2;
    }
    else if(c == 'y' && i == 2)/*forca da gravidade dos corpos 0 e 1 sobre o corpo 2 na coordenada y*/
    {
        f_grav1 = (6.6743e-11*((m2*m0)/((dist1)*(dist1))))*((y0-y2)/(dist1));
        f_grav2 = (6.6743e-11*((m2*m1)/((dist2)*(dist2))))*((y1-y2)/(dist2));

        return f_grav1 + f_grav2;
    }
}

void atualize(double *x, double *y, double *vx, double *vy, double ax, double ay, double dt)
{
    *vx = (*vx) + (dt * ax);
    *vy = (*vy) + (dt * ay);

    *y = (*y) + (dt * (*vy));
    *x = (*x) + (dt * (*vx));
}




