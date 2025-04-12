#ifndef POINT2D_H
#define POINT2D_H

// 2D point
struct Point2D {
    float x;
    float y;
};

// 2d lerp
Point2D lerp(const Point2D& p1, const Point2D& p2, float t);

#endif // POINT2D_H