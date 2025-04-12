// 2D point
struct Point2D {
    float x;
    float y;
};

// 2d lerp
Point2D lerp(const Point2D& p1, const Point2D& p2, float t) {
    return {
        p1.x + t * (p2.x - p1.x),
        p1.y + t * (p2.y - p1.y)
    };
}