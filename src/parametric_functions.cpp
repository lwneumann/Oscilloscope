#include "parametric_functions.h"

void generateSquarePattern(float t, float& x, float& y) {
    if (t < 0.25f) {            // First edge: Move right
        x = t * 4.0f;           // x ranges from 0 to 1
        y = 0.0f;               // y stays at 0
    } else if (t < 0.5f) {      // Second edge: Move up
        x = 1.0f;               // x stays at 1
        y = (t - 0.25f) * 4.0f; // y ranges from 0 to 1
    } else if (t < 0.75f) {     // Third edge: Move left
        x = 1.0f - (t - 0.5f) * 4.0f; // x ranges from 1 to 0
        y = 1.0f;               // y stays at 1
    } else {                    // Fourth edge: Move down
        x = 0.0f;               // x stays at 0
        y = 1.0f - (t - 0.75f) * 4.0f; // y ranges from 1 to 0
    }
}

// Add more parametric functions heree