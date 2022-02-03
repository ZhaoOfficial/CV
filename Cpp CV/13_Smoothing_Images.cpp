#include <iostream>
#include <cstring>
#include <sstream>
#include <cmath>
#include <vector>
#include <initializer_list>

#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

using namespace cv;
using std::string;
using std::complex;
using std::ostream;
using std::stringstream;
using std::vector;
using std::initializer_list;
using std::cin;
using std::cout;
using std::endl;
const string storePath = "D:/Mywork/OpenCV/sampleFile/";
const string samplePath = "D:/Mywork/OpenCV/SampleImage/";



int DELAY_CAPTION = 1500;
int DELAY_BLUR = 100;
int MAX_KERNEL_LENGTH = 31;

Mat src; Mat dst;
string window_name = "Smoothing Demo";
int display_caption(const string caption);
int display_dst(int delay);

int main(int argc, char* argv[])
{
    namedWindow(window_name, WINDOW_AUTOSIZE);
    const string filename = argc >= 2 ? argv[1] : samplePath + "lena.jpg";
    src = imread(filename, IMREAD_COLOR);
    if (src.empty())
    {
        cout << "Error opening image\n";
        cout << " Usage:\n" << argv[0] << "[image_name -- default lena.jpg]\n";
        return EXIT_FAILURE;
    }
    
    int c;

    c = display_caption("Original Image");
    if (c != 0)
        return 0;

    dst = src.clone();
    c = display_dst(DELAY_CAPTION);
    if (c != 0)
        return 0;
    
    c = display_caption("Homogeneous Blur");
    if (c != 0)
        return 0;


    for (int i = 1; i < MAX_KERNEL_LENGTH; i = i + 2)
    {
        blur(src, dst, Size(i, i), Point(-1, -1));
        c = display_dst(DELAY_BLUR);
        if (c != 0)
            return 0;
    }
    c = display_caption("Gaussian Blur");
    if (c != 0)
        return 0;

    for (int i = 1; i < MAX_KERNEL_LENGTH; i = i + 2)
    {
        GaussianBlur(src, dst, Size(i, i), 0, 0);
        c = display_dst(DELAY_BLUR);
        if (c != 0)
            return 0;
    }
    c = display_caption("Median Blur");
    if (c != 0)
        return 0;

    for (int i = 1; i < MAX_KERNEL_LENGTH; i = i + 2)
    {
        medianBlur(src, dst, i);
        c = display_dst(DELAY_BLUR);
        if (c != 0)
            return 0;
    }
    
    c = display_caption("Bilateral Blur");
    if (c != 0)
        return 0;

    for (int i = 1; i < MAX_KERNEL_LENGTH; i = i + 2)
    {
        bilateralFilter(src, dst, i, i * 2, i / 2);
        c = display_dst(DELAY_BLUR);
        if (c != 0)
            return 0;
    }
    display_caption("Done!");
    return 0;
}

int display_caption(const string caption)
{
    dst = Mat::zeros(src.size(), src.type());
    Size captionSize = getTextSize(caption, FONT_HERSHEY_COMPLEX, 1.5, 2, 0);
    Point org((dst.size().width - captionSize.width) / 2, (dst.size().height - captionSize.height) / 2);
    putText(dst, caption, org,
        FONT_HERSHEY_COMPLEX, 1.5, Scalar(255, 255, 255), 2, 8);
    return display_dst(DELAY_CAPTION);
}

int display_dst(int delay)
{
    imshow(window_name, dst);
    int c = waitKey(delay);
    if (c >= 0)
    {
        return -1;
    }
    return 0;
}