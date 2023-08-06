//=============================================================================
// Circular Binary Segmentation
// by Kyle S. Smith
//-----------------------------------------------------------------------------

#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <time.h>
#include "cbs.h"
#include "src/augmented_interval_array.h"
//#include "utilities.c"

//-----------------------------------------------------------------------------

void rsegment(double x[], int start, int end, aiarray_t *L, int shuffles, double p)
{   
    int slice_length = end - start;
    //double tmp_slice_x[slice_length];
    double *tmp_slice_x = malloc(slice_length * sizeof(double));
    double *slice_x = slice_array(tmp_slice_x, x, start, end);
    cbs_stat_t cbs_stat = calculate_cbs(slice_x, slice_length, shuffles, p);

    free(tmp_slice_x);

    int cbs_length = cbs_stat.max_end - cbs_stat.max_start;

    if (cbs_stat.threshold == false || (cbs_length < 5) || (cbs_length == slice_length))
    {
        aiarray_add(L, start, end);
    }
    else
    {
        if (cbs_stat.max_start > 0)
        {
            rsegment(x, start, start + cbs_stat.max_start, L, shuffles, p);
        }
        
        if (cbs_length > 0)
        {
            rsegment(x, start + cbs_stat.max_start, start + cbs_stat.max_end, L, shuffles, p);
        }
        
        if (start + cbs_stat.max_end < end)
        {
            rsegment(x, start + cbs_stat.max_end, end, L, shuffles, p);
        }
    }
}


aiarray_t *calculate_segment(double x[], int length, int shuffles, double p)
{
    int start = 0;
    int end = length;
    aiarray_t *L = aiarray_init();

    srand(time(NULL));

    rsegment(x, start, end, L, shuffles, p);

    return L;
}


aiarray_t *calculate_validate(double x[], int length,  aiarray_t *L, int shuffles, double p)
{
    int i;
    int S[L->nr + 1];
    for (i = 0; i < L->nr; i++)
    {
        S[i] = L->interval_list[i].start;
    }
    S[i] = length;

    aiarray_t *SV = aiarray_init();
    int segment_start = 0;
    int left = 0;
    double t;

    int test;
    for (test = 0; test < L->nr-1; test++)
    { 
        int slice_length = S[test+2] - S[left];
        double *tmp_slice_x = malloc(slice_length * sizeof(double));
        double *slice_x = slice_array(tmp_slice_x, x, S[left], S[test+2]);

        t = calculate_tstat(slice_x, S[test+1]-S[left], slice_length);

        double threshold = 0;
        int thresh_count = 0;
        int site = S[test+1] - S[left];

        //is this needed?
        double *tmp_xt = malloc(slice_length * sizeof(double));
        double *xt = copy_array(tmp_xt, slice_x, slice_length);
        bool flag = true;

        free(tmp_slice_x);

        int k;
        for (k = 0; k < shuffles; k++)
        {
            shuffle_array(xt, slice_length);
            threshold = calculate_tstat(xt, site, slice_length);

            if (threshold > t)
            {
                thresh_count += 1;
            }

            if (thresh_count >= (p * shuffles))
            {
                flag = false;
                break;
            }
        }

        if (flag == true)
        {
            aiarray_add(SV, segment_start, S[test+1]);
            segment_start = S[test+1];
            left += 1;
        }

        free(tmp_xt);
    }
    aiarray_add(SV, segment_start, S[i]);

    return SV;
}