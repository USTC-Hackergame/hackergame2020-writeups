#ifndef MATH_H
#define MATH_H

static inline int abs(int x)
{
    return x < 0 ? -x : x;
}

static inline int max(int a, int b)
{
    return a < b ? b : a;
}

static inline int min(int a, int b)
{
    return b < a ? b : a;
}

#endif
